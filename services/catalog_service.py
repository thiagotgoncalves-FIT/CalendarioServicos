"""
Módulo de serviço para gerenciamento do catálogo de serviços do prestador.
"""
from typing import List, Dict, Any, Tuple
from . import api_client

# Dados mockados em memória para fallback
MOCK_SERVICES = [
    {
        "id": 1,
        "prestador_id": 1,
        "titulo": "Corte Degradê",
        "descricao": "Corte masculino com acabamento na navalha.",
        "preco": 45.0,
        "duracao_minutos": 45,
        "ativo": True,
    },
    {
        "id": 2,
        "prestador_id": 1,
        "titulo": "Barba Terapia",
        "descricao": "Alinhamento e hidratação da barba.",
        "preco": 35.0,
        "duracao_minutos": 30,
        "ativo": True,
    }
]
_mock_id_counter = 3

def get_services(prestador_id: int, token: str = None) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna a lista de serviços do prestador."""
    success, data, status = api_client.get("services", params={"prestador_id": prestador_id}, token=token)
    
    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        return True, [s for s in MOCK_SERVICES if s["prestador_id"] == prestador_id]
    
    if success:
        return True, data if isinstance(data, list) else data.get("items", [])
    return False, []

def create_service(prestador_id: int, titulo: str, preco: float, duracao_minutos: int, descricao: str = "", token: str = None) -> Tuple[bool, Dict[str, Any]]:
    """Cria um novo serviço para o prestador autenticado."""
    payload = {
        "titulo": titulo,
        "descricao": descricao,
        "preco": preco,
        "duracao_minutos": duracao_minutos
    }
    success, data, status = api_client.post("services", json_data=payload, token=token)
    
    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        global _mock_id_counter
        new_service = {
            "id": _mock_id_counter,
            "prestador_id": prestador_id,
            "titulo": titulo,
            "descricao": descricao,
            "preco": preco,
            "duracao_minutos": duracao_minutos,
            "ativo": True
        }
        MOCK_SERVICES.append(new_service)
        _mock_id_counter += 1
        return True, new_service

    if success:
        return True, data
    return False, data

def toggle_service_status(service_id: int, ativo: bool, token: str = None) -> Tuple[bool, Dict[str, Any]]:
    """Ativa ou desativa um serviço."""
    # Usando POST para simular atualização, já que o api_client atual suporta apenas GET/POST
    # No backend real isso poderia ser um PUT /services/{id}
    success, data, status = api_client.post(f"services/{service_id}/toggle", json_data={"ativo": ativo}, token=token)
    
    if not success and isinstance(data, dict) and data.get("mock_fallback"):
        for s in MOCK_SERVICES:
            if s["id"] == service_id:
                s["ativo"] = ativo
                return True, s
        return False, {"message": "Serviço não encontrado no mock."}

    if success:
        return True, data
    return False, data

def get_public_services(token: str = None) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna a lista de serviços ativos disponíveis para visualização pública e de clientes."""
    success, data, status = api_client.get("services", token=token)
    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        return True, [s for s in MOCK_SERVICES if s.get("ativo", True)]
    if success:
        items = data if isinstance(data, list) else data.get("items", [])
        return True, [s for s in items if s.get("ativo", True)]
    return True, [s for s in MOCK_SERVICES if s.get("ativo", True)]
