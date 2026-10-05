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
    - Para role='cliente': cria o registro na tabela user E na tabela cliente (com celular).
    - Para role='prestador': cria apenas o registro na tabela user.
    Retorna: (sucesso: bool, dados_ou_mensagem_erro: dict)
    """
    if not name.strip():
        return False, {"message": "O nome é obrigatório."}
    if not email.strip() or "@" not in email:
        return False, {"message": "Informe um e-mail válido."}
    if not password or len(password) < 3:
        return False, {"message": "A senha deve conter no mínimo 3 caracteres."}
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

    if success and data:
        # Normaliza o response do Xano para o formato esperado pela aplicação
        normalized = _normalize_auth_response(data)

        # Se o usuário for cliente, cria o perfil estendido na tabela `cliente`
        if role == "cliente" and normalized.get("authToken") and normalized.get("user", {}).get("id"):
            _create_cliente_profile(
                user_id=normalized["user"]["id"],
                celular=phone.strip(),
                token=normalized["authToken"]
            )

        if normalized.get("authToken"):
            return True, normalized

    # Fallback mock se Xano não estiver configurado ou retornar vazio
    if _is_mock_fallback(data, status_code) or not data or status_code == 404:
        email_clean = payload["email"]
        if email_clean in _MOCK_USERS_DB:
            return False, {"message": "Este endereço de e-mail já está em uso."}

        new_user = {
            "id": len(_MOCK_USERS_DB) + 1,
            "name": payload["name"],
            "email": email_clean,
            "password": payload["password"],
            "phone": payload["phone"],
            "role": payload["role"],
        }
        _MOCK_USERS_DB[email_clean] = new_user
        mock_token = f"mock_jwt_token_{new_user['id']}_{payload['role']}"
        return True, {
            "authToken": mock_token,
            "user": {k: v for k, v in new_user.items() if k != "password"},
            "_source": "mock_local"
        }

    error_msg = data.get("message") if isinstance(data, dict) else "Erro ao realizar cadastro no Xano."
    return False, {"message": error_msg}


def login(email: str, password: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Autentica um usuário existente.
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

    # Intercepta usuários de demonstração para garantir que sempre funcionem (bypass do Xano)
    email_clean = payload["email"]
    if email_clean in _MOCK_USERS_DB and password == _MOCK_USERS_DB[email_clean]["password"]:
        user_record = _MOCK_USERS_DB[email_clean]
        mock_token = f"mock_jwt_token_{user_record['id']}_{user_record['role']}"
        return True, {
            "authToken": mock_token,
            "user": {k: v for k, v in user_record.items() if k != "password"},
            "_source": "mock_local"
        }

    # Chamada real ao Xano
    success, data, status_code = api_client.post("/auth/login", json_data=payload)

    # LOG TEMPORÁRIO — remover após validar o formato do response do Xano
    import sys
    print(f"[DEBUG LOGIN] success={success} | status={status_code} | data={data}", file=sys.stderr)

    if success and data:
        normalized = _normalize_auth_response(data)
        if normalized.get("authToken"):
            return True, normalized

    # Fallback local se Xano não estiver configurado ou retornar vazio
    if _is_mock_fallback(data, status_code) or not data or status_code == 404:
        email_clean = payload["email"]
        user_record = _MOCK_USERS_DB.get(email_clean)
        if not user_record:
            return False, {"message": "E-mail não cadastrado."}
        if user_record["password"] != password:
            return False, {"message": "Senha incorreta. Verifique suas credenciais."}

        mock_token = f"mock_jwt_token_{user_record['id']}_{user_record['role']}"
        return True, {
            "authToken": mock_token,
            "user": {k: v for k, v in user_record.items() if k != "password"},
            "_source": "mock_local"
        }

    error_msg = data.get("message") if isinstance(data, dict) else "Credenciais inválidas."
    return False, {"message": error_msg}


def get_current_user(token: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Obtém os dados do perfil do usuário associado ao token JWT ativo.
    """
    if not token:
        return False, {"message": "Token de autenticação não fornecido."}

    success, data, status_code = api_client.get("/auth/me", token=token)
    if success:
        return True, data

    # Fallback mock para tokens locais
    if token.startswith("mock_jwt_token_"):
        parts = token.split("_")
        try:
            user_id = int(parts[3])
            for u in _MOCK_USERS_DB.values():
                if u["id"] == user_id:
                    return True, {"user": {k: v for k, v in u.items() if k != "password"}, "_source": "mock_local"}
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
    
    # Chamada real ao Xano
    success, data, status_code = api_client.post("/auth/recover_password", json_data=payload)
    
    if success:
        return True, "As instruções de recuperação foram enviadas para o seu e-mail."
        
    # Fallback local se Xano não estiver configurado
    if _is_mock_fallback(data, status_code) or status_code == 404:
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
    # Guard: resposta vazia ou inválida
    if not data or not isinstance(data, dict):
        return {"authToken": "", "user": {}}

    # Formato esperado: { authToken, user: {...} }
    if "authToken" in data and "user" in data:
        return data

    # Casos onde o token pode vir com chave diferente
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
    Falhas são tratadas silenciosamente (não impede o login).
    """
    payload = {
        "user_id": user_id,
        "celular": celular,
    }
    # Ignora o resultado — a ausência do perfil cliente não deve bloquear o acesso
    api_client.post("/cliente", json_data=payload, token=token)


def _is_mock_fallback(data: Any, status_code: int) -> bool:
    """Verifica se a resposta indica que deve usar o fallback local."""
    return (isinstance(data, dict) and data.get("mock_fallback")) or status_code == 503
