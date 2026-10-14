"""
Cliente de API HTTP para comunicação com o backend Xano.
Encapsula chamadas REST, tratamento de headers JWT e tratamento de erros.
"""

import os
from typing import Any, Dict, Optional, Tuple
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env com override
load_dotenv(override=True)

DEFAULT_API_URL = "https://sua-instancia.xano.io/api:agendai"
API_BASE_URL = os.getenv("XANO_API_URL", DEFAULT_API_URL).rstrip("/")
USE_MOCK_FALLBACK = os.getenv("USE_MOCK_FALLBACK", "True").lower() in ("true", "1", "yes")


def is_placeholder_url(url: str) -> bool:
    """Verifica se a URL configurada ainda é um placeholder demonstrativo."""
    return "sua-instancia.xano.io" in url or not url.startswith("http")


def get_headers(token: Optional[str] = None) -> Dict[str, str]:
    """Monta os cabeçalhos HTTP padrões para as requisições."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def post(endpoint: str, json_data: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> Tuple[bool, Any, int]:
    """
    Executa uma requisição POST na API.
    Retorna: (sucesso: bool, dados_ou_erro: Any, status_code: int)
    """
    clean_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    full_url = f"{API_BASE_URL}{clean_endpoint}"

    # Se a URL não estiver configurada com uma instância real do Xano e mock estiver ativo
    if is_placeholder_url(API_BASE_URL) and USE_MOCK_FALLBACK:
        return False, {"mock_fallback": True, "message": "Instância Xano não configurada. Ativando mock fallback."}, 503

    try:
        response = requests.post(
            full_url,
            json=json_data or {},
            headers=get_headers(token),
            timeout=10
        )
        status_code = response.status_code
        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}

        is_success = 200 <= status_code < 300
        return is_success, data, status_code

    except requests.exceptions.RequestException as e:
        return False, {"message": f"Erro de conexão com o servidor Xano: {str(e)}"}, 500


def get(endpoint: str, params: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> Tuple[bool, Any, int]:
    """
    Executa uma requisição GET na API.
    Retorna: (sucesso: bool, dados_ou_erro: Any, status_code: int)
    """
    clean_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    full_url = f"{API_BASE_URL}{clean_endpoint}"

    if is_placeholder_url(API_BASE_URL) and USE_MOCK_FALLBACK:
        return False, {"mock_fallback": True, "message": "Instância Xano não configurada. Ativando mock fallback."}, 503

    try:
        response = requests.get(
            full_url,
            params=params,
            headers=get_headers(token),
            timeout=10
        )
        status_code = response.status_code
        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}

        is_success = 200 <= status_code < 300
        return is_success, data, status_code

    except requests.exceptions.RequestException as e:
        return False, {"message": f"Erro de conexão com o servidor Xano: {str(e)}"}, 500
