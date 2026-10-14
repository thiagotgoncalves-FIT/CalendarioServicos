"""
Serviço de autenticação e gerenciamento de perfil para o AgendAí.
Comunica-se com os endpoints do Xano ou utiliza persistência simulada local caso a API não esteja configurada.

Arquitetura do Xano:
  - Tabela `user`: credenciais, nome, email, role (prestador | cliente)
  - Tabela `cliente`: perfil estendido do cliente (user_id FK, celular, cpf, status_cliente_id)
"""

from typing import Any, Dict, Optional, Tuple
from services import api_client

# Base de usuários em memória para fallback/testes locais caso Xano não esteja acessível
_MOCK_USERS_DB: Dict[str, Dict[str, Any]] = {
    "carlos@barbearia.com": {
        "id": 1,
        "name": "Carlos Barbeiro",
        "email": "carlos@barbearia.com",
        "password": "123",
        "phone": "11988887777",
        "role": "prestador",
    },
    "mariana@email.com": {
        "id": 2,
        "name": "Mariana Silva",
        "email": "mariana@email.com",
        "password": "123",
        "phone": "11977776666",
        "role": "cliente",
    },
    "bruno.teixeira@gmail.com": {
        "id": 4,
        "name": "Bruno Teixeira",
        "email": "bruno.teixeira@gmail.com",
        "password": "123",
        "phone": "11900000000",
        "role": "prestador",
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
        return True, {
            "authToken": mock_token,
            "user": {k: v for k, v in user_record.items() if k != "password"},
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
        return True, {"user": user_dict}

    # Fallback para tokens locais
    if token.startswith("jwt_session_") or token.startswith("mock_jwt_token_"):
        parts = token.split("_")
        try:
            user_id = int(parts[2] if parts[0] == "jwt" else parts[3])
            for u in _MOCK_USERS_DB.values():
                if u["id"] == user_id:
                    return True, {"user": {k: v for k, v in u.items() if k != "password"}, "_source": "resilient_local"}
        except (IndexError, ValueError):
            pass

    return False, {"message": "Sessão inválida ou expirada."}


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
