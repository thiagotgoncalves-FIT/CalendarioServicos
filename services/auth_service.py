"""
Serviço de autenticação e gerenciamento de perfil para o AgendAí.
Comunica-se com os endpoints do Xano ou utiliza persistência simulada local caso a API não esteja configurada.
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

    # Tenta chamada real na API do Xano
    success, data, status_code = api_client.post("/auth/signup", json_data=payload)

    if success:
        return True, data

    # Se a resposta indicar fallback de desenvolvimento ou falha de conexão inicial
    if isinstance(data, dict) and data.get("mock_fallback") or status_code == 503:
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
            "user": {
                "id": new_user["id"],
                "name": new_user["name"],
                "email": new_user["email"],
                "phone": new_user["phone"],
                "role": new_user["role"],
            },
            "_source": "mock_local"
        }

    # Tratamento de erro retornado pela API real
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

    # Tenta chamada real no Xano
    success, data, status_code = api_client.post("/auth/login", json_data=payload)

    if success:
        return True, data

    # Fallback local se Xano não estiver configurado
    if isinstance(data, dict) and data.get("mock_fallback") or status_code == 503:
        email_clean = payload["email"]
        user_record = _MOCK_USERS_DB.get(email_clean)
        if not user_record:
            return False, {"message": "E-mail não cadastrado."}
        if user_record["password"] != password:
            return False, {"message": "Senha incorreta. Verifique suas credenciais."}

        mock_token = f"mock_jwt_token_{user_record['id']}_{user_record['role']}"
        return True, {
            "authToken": mock_token,
            "user": {
                "id": user_record["id"],
                "name": user_record["name"],
                "email": user_record["email"],
                "phone": user_record["phone"],
                "role": user_record["role"],
            },
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

    if token.startswith("mock_jwt_token_"):
        parts = token.split("_")
        user_id = int(parts[3])
        for u in _MOCK_USERS_DB.values():
            if u["id"] == user_id:
                return True, {"user": u, "_source": "mock_local"}

    return False, {"message": "Sessão inválida ou expirada."}
