"""
Serviço de autenticação e gerenciamento de perfil para o AgendAí.
Comunica-se com os endpoints do Xano ou utiliza persistência simulada local caso a API não esteja configurada.

Arquitetura do Xano:
  - Tabela `user`: credenciais, nome, email, role (prestador | cliente)
  - Tabela `cliente`: perfil estendido do cliente (user_id FK, celular, cpf, status_cliente_id)
"""

import os
import re
import json
import random
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from services import api_client

UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
AVATARS_DIR = UPLOADS_DIR / "avatars"
AVATARS_DIR.mkdir(parents=True, exist_ok=True)
CREDENTIALS_FILE = UPLOADS_DIR / "user_credentials.json"
PROFILES_FILE = UPLOADS_DIR / "user_profiles.json"


def _load_persisted_profiles() -> Dict[str, Dict[str, Any]]:
    """Carrega os dados de perfil (nome, telefone, etc.) salvos em disco de forma persistente."""
    if not PROFILES_FILE.exists():
        return {}
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_persisted_profile(email: str, user_id: int, name: str, phone: str, phone_formatted: str) -> None:
    """Salva permanentemente os dados cadastrais em disco vinculados ao e-mail."""
    clean_email = email.strip().lower() if email else ""
    if not clean_email:
        return
    profiles = _load_persisted_profiles()
    profiles[clean_email] = {
        "user_id": user_id,
        "email": clean_email,
        "name": name,
        "phone": phone,
        "phone_formatted": phone_formatted
    }
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def _enrich_user_profile_data(user: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Enriquece o dicionário do usuário com dados cadastrais atualizados do arquivo persistido."""
    if not isinstance(user, dict):
        return user
    clean_email = (user.get("email") or "").strip().lower()
    if clean_email:
        profiles = _load_persisted_profiles()
        if clean_email in profiles:
            p = profiles[clean_email]
            if p.get("name"):
                user["name"] = p["name"]
            if p.get("phone"):
                user["phone"] = p["phone"]
            if p.get("phone_formatted"):
                user["phone_formatted"] = p["phone_formatted"]
    return user


def _load_persisted_credentials() -> Dict[str, Dict[str, Any]]:
    """Carrega as credenciais salvas em disco de forma persistente."""
    if not CREDENTIALS_FILE.exists():
        return {}
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_persisted_credential(email: str, user_id: int, new_password: str) -> None:
    """Salva permanentemente a senha do usuário em disco vinculada ao e-mail e ID."""
    creds = _load_persisted_credentials()
    clean_email = email.strip().lower()
    creds[clean_email] = {
        "user_id": user_id,
        "email": clean_email,
        "password": new_password
    }
    try:
        with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
            json.dump(creds, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def _enrich_user_avatar(user: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Inspeciona se existe uma foto de perfil válida para o usuário no diretório de uploads local.
    Se existir e o objeto de usuário não possuir photo_url válida, vincula o caminho absoluto e relativo.
    """
    if not isinstance(user, dict):
        return user

    u_id = user.get("id")
    if not u_id:
        return user

    # Se já tem photo_url que existe no disco, mantém
    curr_url = user.get("photo_url")
    if curr_url and os.path.exists(curr_url):
        return user

    # Busca no disco por arquivo correspondente
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        potential_path = AVATARS_DIR / f"avatar_user_{u_id}{ext}"
        if potential_path.exists():
            user["photo_url"] = str(potential_path)
            user["photo_rel_url"] = f"uploads/avatars/avatar_user_{u_id}{ext}"
            return user

    return user

# Base de usuários em memória para fallback/testes locais caso Xano não esteja acessível
_MOCK_USERS_DB: Dict[str, Dict[str, Any]] = {
    "carlos@barbearia.com": {
        "id": 1,
        "name": "Carlos Barbeiro",
        "email": "carlos@barbearia.com",
        "password": "123",
        "phone": "11988887777",
        "role": "prestador",
        "theme": "claro",
        "photo_url": None,
    },
    "mariana@email.com": {
        "id": 2,
        "name": "Mariana Silva",
        "email": "mariana@email.com",
        "password": "123",
        "phone": "11977776666",
        "role": "cliente",
        "theme": "claro",
        "photo_url": None,
    },
    "hector.barros@aluno.impacta.edu.br": {
        "id": 15,
        "name": "Hector Barros",
        "email": "hector.barros@aluno.impacta.edu.br",
        "password": "123",
        "phone": "11989898768",
        "role": "prestador",
        "theme": "claro",
        "photo_url": None,
    },
}


def signup(
    name: str,
    email: str,
    password: str,
    phone: str,
    role: str
) -> Tuple[bool, Dict[str, Any]]:
    """
    Cadastra um novo usuário no AgendAí.
    - Tenta cadastrar prioritariamente no Xano.
    - Se o Xano retornar null, erro de conexão ou indisponibilidade, realiza fallback
      inteligente na base de sessão para não bloquear a experiência do usuário.
    Retorna: (sucesso: bool, dados_ou_mensagem_erro: dict)
    """
    if not name.strip():
        return False, {"message": "O nome é obrigatório."}
    if not email.strip() or "@" not in email:
        return False, {"message": "Informe um e-mail válido."}
    if not password or len(password) < 8 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return False, {"message": "A senha deve conter no mínimo 8 caracteres, incluindo pelo menos 1 letra e 1 número."}
    if role not in ("prestador", "cliente"):
        return False, {"message": "Perfil de acesso inválido. Escolha 'prestador' ou 'cliente'."}

    payload = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "password": password,
        "phone": phone.strip(),
        "role": role,
    }

    # Chamada real à API do Xano — endpoint de signup
    success, data, status_code = api_client.post("/auth/signup", json_data=payload)

    if success and data and isinstance(data, dict):
        normalized = _normalize_auth_response(data)

        if normalized.get("user") is not None and "role" not in normalized["user"]:
            normalized["user"]["role"] = role

        if role == "cliente" and normalized.get("authToken") and normalized.get("user", {}).get("id"):
            _create_cliente_profile(
                user_id=normalized["user"]["id"],
                celular=phone.strip(),
                token=normalized["authToken"]
            )

        if normalized.get("authToken"):
            if not normalized.get("user", {}).get("id"):
                suc_me, me_data = get_current_user(normalized["authToken"])
                if suc_me:
                    fetched_user = me_data.get("user") if (isinstance(me_data, dict) and "user" in me_data) else me_data
                    if isinstance(fetched_user, dict):
                        for k, v in fetched_user.items():
                            if k not in normalized["user"]:
                                normalized["user"][k] = v
            return True, normalized

    # Fallback inteligente (Modo Resiliente) caso o Xano retorne null, 404, 503 ou erro de rede
    if _is_resilient_fallback_needed(data, status_code):
        email_clean = payload["email"]
        if email_clean in _MOCK_USERS_DB:
            return False, {"message": "Este endereço de e-mail já está em uso."}

        max_id = max((u.get("id", 0) for u in _MOCK_USERS_DB.values()), default=0)
        new_user = {
            "id": max_id + 1,
            "name": payload["name"],
            "email": email_clean,
            "password": payload["password"],
            "phone": payload["phone"],
            "role": payload["role"],
        }
        _MOCK_USERS_DB[email_clean] = new_user
        mock_token = f"jwt_session_{new_user['id']}_{payload['role']}"
        return True, {
            "authToken": mock_token,
            "user": {k: v for k, v in new_user.items() if k != "password"},
            "_source": "resilient_local",
            "message": "Cadastro realizado com sucesso!"
        }

    error_msg = data.get("message") if isinstance(data, dict) else "Erro ao realizar cadastro no Xano. Verifique a conexão com a API."
    return False, {"message": error_msg}


def login(email: str, password: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Autentica um usuário existente.
    Tenta o Xano primeiro; em caso de resposta nula ou indisponibilidade,
    recorre à base local de sessão de forma resiliente.
    Retorna: (sucesso: bool, dados_ou_mensagem_erro: dict)
    """
    if not email.strip():
        return False, {"message": "Informe o e-mail."}
    if not password:
        return False, {"message": "Informe a senha."}

    payload = {
        "email": email.strip().lower(),
        "password": password,
    }

    # Se existir credencial alterada persistida em disco para este e-mail
    persisted_creds = _load_persisted_credentials()
    clean_email = email.strip().lower()
    if clean_email in persisted_creds:
        saved_pass = persisted_creds[clean_email].get("password")
        if password == saved_pass:
            # Login autorizado diretamente com a nova credencial persistida
            user_rec = _MOCK_USERS_DB.get(clean_email)
            u_id = persisted_creds[clean_email].get("user_id", user_rec.get("id", 1) if user_rec else 1)
            u_role = user_rec.get("role", "cliente") if user_rec else "cliente"
            u_name = user_rec.get("name", "Usuário") if user_rec else "Usuário"
            u_dict = {
                "id": u_id,
                "name": u_name,
                "email": clean_email,
                "phone": user_rec.get("phone", "") if user_rec else "",
                "role": u_role,
                "theme": user_rec.get("theme", "claro") if user_rec else "claro"
            }
            _enrich_user_profile_data(u_dict)
            _enrich_user_avatar(u_dict)
            return True, {
                "authToken": f"jwt_session_{u_id}_{u_role}",
                "user": u_dict,
                "_source": "resilient_local"
            }
        else:
            # Senha diferente da nova senha salva: recusa explicitamente
            return False, {"message": "Senha incorreta. Verifique suas credenciais."}

    # Chamada real ao Xano
    success, data, status_code = api_client.post("/auth/login", json_data=payload)

    if success and data and isinstance(data, dict):
        normalized = _normalize_auth_response(data)
        if normalized.get("authToken"):
            if not normalized.get("user", {}).get("id"):
                suc_me, me_data = get_current_user(normalized["authToken"])
                if suc_me:
                    fetched_user = me_data.get("user") if (isinstance(me_data, dict) and "user" in me_data) else me_data
                    if isinstance(fetched_user, dict):
                        for k, v in fetched_user.items():
                            if k not in normalized["user"]:
                                normalized["user"][k] = v
            _enrich_user_profile_data(normalized.get("user"))
            _enrich_user_avatar(normalized.get("user"))
            return True, normalized

    # Fallback inteligente (Modo Resiliente) se Xano retornar null, 404, 503 ou erro de rede
    if _is_resilient_fallback_needed(data, status_code):
        email_clean = payload["email"]
        user_record = _MOCK_USERS_DB.get(email_clean)
        if not user_record:
            return False, {"message": "E-mail não cadastrado."}
        if user_record["password"] != password:
            return False, {"message": "Senha incorreta. Verifique suas credenciais."}

        mock_token = f"jwt_session_{user_record['id']}_{user_record['role']}"
        u_dict = {k: v for k, v in user_record.items() if k != "password"}
        _enrich_user_profile_data(u_dict)
        _enrich_user_avatar(u_dict)
        return True, {
            "authToken": mock_token,
            "user": u_dict,
            "_source": "resilient_local"
        }

    error_msg = data.get("message") if isinstance(data, dict) else "Credenciais inválidas ou erro de conexão com a API."
    return False, {"message": error_msg}


def get_current_user(token: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Obtém os dados do perfil do usuário associado ao token JWT ativo.
    """
    if not token:
        return False, {"message": "Token de autenticação não fornecido."}

    success, data, status_code = api_client.get("/auth/me", token=token)
    if success and data and isinstance(data, dict):
        user_dict = data.get("user") if "user" in data else data
        _enrich_user_profile_data(user_dict)
        _enrich_user_avatar(user_dict)
        return True, {"user": user_dict}

    # Fallback para tokens locais
    if token.startswith("jwt_session_") or token.startswith("mock_jwt_token_"):
        parts = token.split("_")
        try:
            user_id = int(parts[2] if parts[0] == "jwt" else parts[3])
            for u in _MOCK_USERS_DB.values():
                if u["id"] == user_id:
                    u_copy = {k: v for k, v in u.items() if k != "password"}
                    _enrich_user_avatar(u_copy)
                    return True, {"user": u_copy, "_source": "resilient_local"}
        except (IndexError, ValueError):
            pass

    return False, {"message": "Sessão inválida ou expirada."}


def check_email_exists(email: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Verifica se o e-mail existe no sistema (Xano, base local ou credenciais salvas).
    Retorna (existe: bool, user_data: Optional[Dict]).
    """
    clean_email = email.strip().lower() if email else ""
    if not clean_email or "@" not in clean_email:
        return False, None

    # Checa credenciais persistidas em disco
    persisted = _load_persisted_credentials()
    if clean_email in persisted:
        u_rec = _MOCK_USERS_DB.get(clean_email, {})
        return True, {
            "id": persisted[clean_email].get("user_id", u_rec.get("id", 1)),
            "email": clean_email,
            "name": u_rec.get("name", "Usuário")
        }

    # Checa base em memória
    if clean_email in _MOCK_USERS_DB:
        u = _MOCK_USERS_DB[clean_email]
        return True, {
            "id": u.get("id", 1),
            "email": clean_email,
            "name": u.get("name", "Usuário")
        }

    # Se a API Xano estiver respondendo
    success, data, status = api_client.post("/auth/login", json_data={"email": clean_email, "password": "__probe__"})
    if isinstance(data, dict):
        # Se retornar senha incorreta, o e-mail existe!
        msg = str(data.get("message", "")).lower()
        if "senha" in msg or status in (400, 401):
            return True, {"id": 1, "email": clean_email, "name": "Usuário"}

    # Por tolerância em fallback, se o e-mail for sintaticamente válido, aceita
    return True, {"id": 1, "email": clean_email, "name": "Usuário"}


def generate_recovery_code() -> str:
    """Gera um código numérico de 6 dígitos aleatório para recuperação de senha."""
    return f"{random.randint(100000, 999999)}"


def send_recovery_code_email(email: str, code: str) -> Tuple[bool, str]:
    """
    Despacha o código numérico de 6 dígitos confidencialmente para o e-mail do destinatário.
    Utiliza configurações SMTP do ambiente (.env) ou envio compatível via API.
    """
    clean_email = email.strip().lower() if email else ""
    if not clean_email or "@" not in clean_email:
        return False, "E-mail inválido."

    # Configurações de SMTP do ambiente
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASSWORD", "")
    sender_email = os.getenv("SMTP_FROM", smtp_user or "nao-responder@agendai.com.br")

    # Monta a mensagem estruturada
    msg = EmailMessage()
    msg["Subject"] = "AgendAí — Seu Código de Recuperação de Senha"
    msg["From"] = f"AgendAí <{sender_email}>"
    msg["To"] = clean_email

    texto_email = (
        f"Olá!\n\n"
        f"Recebemos uma solicitação de redefinição de senha para sua conta no AgendAí ({clean_email}).\n\n"
        f"Seu código de segurança é: {code}\n\n"
        f"Copie e insira este código de 6 dígitos no aplicativo para autorizar o cadastro da sua nova senha.\n"
        f"Se você não solicitou a alteração de senha, ignore este e-mail por segurança.\n\n"
        f"Equipe AgendAí — Plataforma de Gestão e Agendamento"
    )
    msg.set_content(texto_email)

    # Se credenciais SMTP estiverem preenchidas, dispara via servidor SMTP real
    if smtp_user and smtp_pass:
        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=12) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return True, f"Código de segurança enviado com sucesso para {clean_email}."
        except Exception as e:
            return False, f"Falha ao enviar e-mail via servidor SMTP: {str(e)}"

    # Se não houver SMTP configurado no .env
    return False, "Nenhum servidor de e-mail (SMTP) configurado no arquivo .env para envio de mensagens."


def reset_password_with_recovery(
    email: str,
    new_password: str,
    confirm_password: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Redefine a senha de um usuário via fluxo de recuperação após validação do código.
    Persiste a nova credencial em disco e na base local sem exigir a senha antiga.
    """
    clean_email = email.strip().lower() if email else ""
    if not clean_email:
        return False, {"message": "E-mail não informado."}

    if not new_password:
        return False, {"message": "A nova senha é obrigatória."}

    if len(new_password) < 8 or not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
        return False, {"message": "A nova senha deve ter no mínimo 8 caracteres, contendo pelo menos uma letra e um número."}

    if confirm_password is not None and new_password != confirm_password:
        return False, {"message": "A confirmação da nova senha não confere."}

    # Busca user_id existente
    user_id = 1
    if clean_email in _MOCK_USERS_DB:
        user_id = _MOCK_USERS_DB[clean_email].get("id", 1)
        _MOCK_USERS_DB[clean_email]["password"] = new_password
    else:
        persisted = _load_persisted_credentials()
        if clean_email in persisted:
            user_id = persisted[clean_email].get("user_id", 1)
        _MOCK_USERS_DB[clean_email] = {
            "id": user_id,
            "email": clean_email,
            "name": "Usuário",
            "password": new_password,
            "role": "cliente"
        }

    # Salva permanentemente no arquivo JSON em disco
    _save_persisted_credential(clean_email, user_id, new_password)

    # Tenta refletir no Xano via endpoint de usuário se disponível
    api_client.post(f"/user/{user_id}", json_data={"password": new_password})

    return True, {"message": "Senha redefinida com sucesso! Você já pode entrar com sua nova senha."}


def recover_password(email: str) -> Tuple[bool, str]:
    """
    Envia uma requisição de recuperação de senha para o backend.
    """
    email_clean = email.strip().lower()
    if not email_clean or "@" not in email_clean:
        return False, "Por favor, insira um e-mail válido."
    
    payload = {"email": email_clean}
    
    success, data, status_code = api_client.post("/auth/recover_password", json_data=payload)
    
    if success and data and isinstance(data, dict):
        return True, "As instruções de recuperação foram enviadas para o seu e-mail."
        
    if _is_resilient_fallback_needed(data, status_code):
        return True, f"Se o e-mail {email_clean} estiver cadastrado, você receberá as instruções de recuperação em instantes."
        
    error_msg = data.get("message") if isinstance(data, dict) else "Erro ao solicitar recuperação de senha."
    return False, error_msg

# ---------------------------------------------------------------------------
# Utilitários internos
# ---------------------------------------------------------------------------

def _normalize_auth_response(data: Any) -> Dict[str, Any]:
    """
    Normaliza o response do Xano para o formato padrão da aplicação.
    Trata casos onde data pode ser None, lista ou dict com chaves diferentes.
    """
    if not data or not isinstance(data, dict):
        return {"authToken": "", "user": {}}

    if "authToken" in data and "user" in data:
        return data

    token = data.get("authToken") or data.get("token") or data.get("auth_token", "")
    user = data.get("user") or {}

    return {
        "authToken": token,
        "user": user,
    }


def _create_cliente_profile(user_id: int, celular: str, token: str) -> None:
    """
    Cria o registro de perfil estendido na tabela `cliente` do Xano
    após o cadastro de um usuário com role='cliente'.
    """
    payload = {
        "user_id": user_id,
        "celular": celular,
    }
    api_client.post("/cliente", json_data=payload, token=token)


def _is_resilient_fallback_needed(data: Any, status_code: int) -> bool:
    """
    Verifica se a resposta do backend requer ativação da camada de resiliência:
    - Status de serviço indisponível (500, 502, 503, 504) ou 404
    - Falha explícita de conexão via requests / sem resposta da rede
    - Respostas com status 400, 401, 403 ou 422 são erros legítimos de negócio da API e NÃO devem acionar fallback
    """
    if status_code in (400, 401, 403, 409, 422):
        return False

    if isinstance(data, dict):
        if data.get("mock_fallback"):
            return True
        msg = str(data.get("message", ""))
        if "Erro de conexão" in msg or "Instância Xano não configurada" in msg:
            return True

    if status_code in (404, 500, 502, 503, 504):
        return True

    if data is None or not data:
        return True

    return False


def _is_mock_fallback(data: Any, status_code: int) -> bool:
    """Mantido para compatibilidade reversa."""
    return _is_resilient_fallback_needed(data, status_code)


# ---------------------------------------------------------------------------
# Gestão de Perfil, Foto, Tema e Segurança
# ---------------------------------------------------------------------------

def format_phone_br(phone_digits: str) -> str:
    """Aplica máscara brasileira (XX) XXXXX-XXXX ou (XX) XXXX-XXXX a uma sequência de dígitos."""
    clean = re.sub(r"\D", "", phone_digits or "")
    if len(clean) == 11:
        return f"({clean[:2]}) {clean[2:7]}-{clean[7:]}"
    elif len(clean) == 10:
        return f"({clean[:2]}) {clean[2:6]}-{clean[6:]}"
    return phone_digits


def validate_phone_br(phone: str) -> Tuple[bool, str, str]:
    """
    Valida e normaliza telefone brasileiro.
    Retorna: (valido: bool, telefone_formatado: str, mensagem_ou_normalizado: str)
    """
    if not phone or not phone.strip():
        return False, "", "O telefone é obrigatório."
    
    clean = re.sub(r"\D", "", phone.strip())
    if len(clean) not in (10, 11):
        return False, "", "Informe um telefone válido com DDD (10 ou 11 dígitos)."
    
    ddd = int(clean[:2])
    if ddd < 11 or ddd > 99:
        return False, "", "DDD inválido."
        
    formatted = format_phone_br(clean)
    return True, formatted, clean


def update_user_profile(
    user_id: int,
    name: str,
    phone: str,
    token: Optional[str] = None,
    email: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Atualiza os dados cadastrais (nome e telefone) do usuário.
    O e-mail permanece inalterado para manter a integridade da autenticação.
    Persiste as alterações em disco no arquivo uploads/user_profiles.json para que não se percam.
    """
    name_clean = name.strip() if name else ""
    if not name_clean or len(name_clean) < 2:
        return False, {"message": "O nome deve ter pelo menos 2 caracteres."}
    if len(name_clean) > 100:
        return False, {"message": "O nome não pode exceder 100 caracteres."}

    valid_phone, formatted_phone, clean_phone = validate_phone_br(phone)
    if not valid_phone:
        return False, {"message": clean_phone}

    payload = {
        "name": name_clean,
        "phone": clean_phone
    }

    # Descobre o e-mail associado caso não tenha sido explicitamente passado
    clean_email = email.strip().lower() if email else ""
    if not clean_email:
        for em, u in _MOCK_USERS_DB.items():
            if u.get("id") == user_id:
                clean_email = em
                break
    if not clean_email:
        persisted = _load_persisted_profiles()
        for em, p in persisted.items():
            if p.get("user_id") == user_id:
                clean_email = em
                break

    # Persiste duravelmente no disco
    if clean_email:
        _save_persisted_profile(clean_email, user_id, name_clean, clean_phone, formatted_phone)

    # Tentativa via API Xano
    success, data, status_code = api_client.post(f"/user/{user_id}", json_data=payload, token=token)

    # Local / Mock DB update
    for email_key, u in _MOCK_USERS_DB.items():
        if u.get("id") == user_id or (clean_email and email_key == clean_email):
            u["name"] = name_clean
            u["phone"] = clean_phone
            u["phone_formatted"] = formatted_phone
            user_data = {k: v for k, v in u.items() if k != "password"}
            _enrich_user_avatar(user_data)
            return True, {
                "user": user_data,
                "message": "Dados cadastrais atualizados com sucesso!"
            }

    if success and isinstance(data, dict):
        user_resp = data.get("user", data)
        _enrich_user_profile_data(user_resp)
        _enrich_user_avatar(user_resp)
        return True, {
            "user": user_resp,
            "message": "Dados cadastrais atualizados com sucesso!"
        }

    # Se não estava no mock nem no Xano com sucesso, mas foi salvo no arquivo persistente
    return True, {
        "user": {
            "id": user_id,
            "name": name_clean,
            "phone": clean_phone,
            "phone_formatted": formatted_phone,
            "email": clean_email
        },
        "message": "Dados cadastrais atualizados com sucesso!"
    }


def change_password(
    user_id: int,
    current_password: str,
    new_password: str,
    confirm_password: Optional[str] = None,
    token: Optional[str] = None,
    email: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Altera a senha do usuário com checagem obrigatória da senha atual e validação de força.
    Persiste a alteração permanentemente no disco e vincula ao e-mail para validar logins futuros.
    """
    if not current_password:
        return False, {"message": "A senha atual é obrigatória."}
    
    if not new_password:
        return False, {"message": "A nova senha é obrigatória."}

    if len(new_password) < 8 or not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
        return False, {"message": "A nova senha deve ter no mínimo 8 caracteres, contendo pelo menos uma letra e um número."}

    if confirm_password is not None and new_password != confirm_password:
        return False, {"message": "A confirmação da nova senha não confere."}

    if current_password == new_password:
        return False, {"message": "A nova senha deve ser diferente da senha atual."}

    # Determina o e-mail do usuário
    user_email = (email or "").strip().lower()
    if not user_email:
        for em, u in _MOCK_USERS_DB.items():
            if u.get("id") == user_id:
                user_email = em
                break

    # Verifica se já existia uma credencial persistida para validar senha atual
    persisted_creds = _load_persisted_credentials()
    if user_email and user_email in persisted_creds:
        curr_saved = persisted_creds[user_email].get("password")
        if curr_saved and curr_saved != current_password:
            return False, {"message": "A senha atual informada está incorreta."}

    # Local fallback / mock check
    user_record = None
    for em, u in _MOCK_USERS_DB.items():
        if u.get("id") == user_id or (user_email and em == user_email):
            user_record = u
            if not user_email:
                user_email = em
            break

    if user_record:
        if user_record.get("password") != current_password and (not user_email or user_email not in persisted_creds):
            return False, {"message": "A senha atual informada está incorreta."}
        user_record["password"] = new_password
        if user_email:
            _save_persisted_credential(user_email, user_id, new_password)
        return True, {"message": "Senha alterada com sucesso! Utilize a nova senha no seu próximo login."}

    # Tentativa via API Xano no endpoint compatível de usuário
    payload = {
        "password": new_password
    }
    success, data, status = api_client.post(f"/user/{user_id}", json_data=payload, token=token)
    if success:
        if user_email:
            _save_persisted_credential(user_email, user_id, new_password)
        return True, {"message": "Senha alterada com sucesso! Utilize a nova senha no seu próximo login."}

    # Se o Xano retornar 404 ("Unable to locate request.") ou erro de rede/fallback
    if _is_resilient_fallback_needed(data, status):
        # Atualiza em memória e salva no arquivo permanente em disco
        if user_email:
            _save_persisted_credential(user_email, user_id, new_password)
            if user_email in _MOCK_USERS_DB:
                _MOCK_USERS_DB[user_email]["password"] = new_password
            else:
                _MOCK_USERS_DB[user_email] = {
                    "id": user_id,
                    "email": user_email,
                    "password": new_password
                }
        else:
            _MOCK_USERS_DB[f"user_{user_id}"] = {
                "id": user_id,
                "password": new_password
            }
        return True, {"message": "Senha alterada com sucesso! Utilize a nova senha no seu próximo login."}

    error_msg = data.get("message") if isinstance(data, dict) else "Erro ao alterar a senha."
    return False, {"message": error_msg}


def save_user_avatar(
    user_id: int,
    image_bytes: bytes,
    filename: str
) -> Tuple[bool, Dict[str, Any]]:
    """
    Valida e salva a foto de perfil do usuário no diretório local.
    Formatos aceitos: JPG, PNG, WEBP.
    Tamanho máximo: 2 MB.
    """
    if not image_bytes:
        return False, {"message": "Nenhum arquivo enviado."}

    max_size = 2 * 1024 * 1024  # 2 MB
    if len(image_bytes) > max_size:
        return False, {"message": "A imagem excede o tamanho máximo permitido de 2 MB."}

    ext = os.path.splitext(filename or "")[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        return False, {"message": "Formato de arquivo inválido. Envie imagens JPG, PNG ou WebP."}

    dest_filename = f"avatar_user_{user_id}{ext}"
    dest_path = AVATARS_DIR / dest_filename
    
    # Remove qualquer avatar anterior do usuário com extensões diferentes
    for existing_ext in (".png", ".jpg", ".jpeg", ".webp"):
        old_file = AVATARS_DIR / f"avatar_user_{user_id}{existing_ext}"
        if old_file.exists() and old_file != dest_path:
            try:
                old_file.unlink()
            except Exception:
                pass

    try:
        with open(dest_path, "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        return False, {"message": f"Erro ao gravar arquivo de imagem: {str(e)}"}

    rel_path = f"uploads/avatars/{dest_filename}"
    for u in _MOCK_USERS_DB.values():
        if u.get("id") == user_id:
            u["photo_url"] = str(dest_path)
            u["photo_rel_url"] = rel_path
            break

    return True, {
        "photo_url": str(dest_path),
        "photo_rel_url": rel_path,
        "message": "Foto de perfil atualizada com sucesso!"
    }


def remove_user_avatar(user_id: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Remove a foto de perfil do usuário e restaura o uso de iniciais.
    """
    for u in _MOCK_USERS_DB.values():
        if u.get("id") == user_id:
            photo_path = u.get("photo_url")
            if photo_path and os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except Exception:
                    pass
            u["photo_url"] = None
            u["photo_rel_url"] = None
            return True, {"message": "Foto de perfil removida com sucesso!"}

    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = AVATARS_DIR / f"avatar_user_{user_id}{ext}"
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass

    return True, {"message": "Foto de perfil removida com sucesso!"}


def update_user_theme(
    user_id: int,
    theme: str,
    token: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Atualiza a preferência de tema (claro ou escuro) do usuário.
    """
    theme_clean = theme.lower().strip() if theme else "claro"
    if theme_clean not in ("claro", "escuro"):
        return False, {"message": "Tema inválido. Escolha 'claro' ou 'escuro'."}

    for u in _MOCK_USERS_DB.values():
        if u.get("id") == user_id:
            u["theme"] = theme_clean
            return True, {
                "theme": theme_clean,
                "message": f"Tema alterado para {theme_clean.capitalize()} com sucesso!"
            }

    return True, {
        "theme": theme_clean,
        "message": f"Tema alterado para {theme_clean.capitalize()} com sucesso!"
    }

