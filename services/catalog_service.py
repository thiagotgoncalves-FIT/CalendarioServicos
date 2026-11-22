"""
Módulo de serviço para gerenciamento do catálogo de serviços do prestador.
"""
from typing import List, Dict, Any, Tuple
from . import api_client

# Dados mockados em memória para fallback
MOCK_SERVICES = [
    {
        "id": 1,
        "prestador_id": 15,
        "titulo": "Corte Masculino & Barba",
        "descricao": "Atendimento completo com corte degradê e alinhamento de barba na navalha.",
        "preco": 60.0,
        "duracao_minutos": 45,
        "ativo": True
    },
    {
        "id": 2,
        "prestador_id": 15,
        "titulo": "Barboterapia Relaxante",
        "descricao": "Toalha quente, massagem facial e hidratação de barba com óleos essenciais.",
        "preco": 40.0,
        "duracao_minutos": 30,
        "ativo": True
    }
]
_mock_id_counter = 3

def get_services(prestador_id: int, token: str = None) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna a lista de serviços do prestador."""
    success, data, status = api_client.get("services", params={"prestador_id": str(prestador_id)}, token=token)
    
    if not success and (status in (404, 500, 502, 503) or (isinstance(data, dict) and data.get("mock_fallback")) or status == 0):
        return True, [s for s in MOCK_SERVICES if str(s["prestador_id"]) == str(prestador_id)]
    
    if success:
        return True, data if isinstance(data, list) else data.get("items", [])
    return False, []

def create_service(prestador_id: int, titulo: str, preco: float, duracao_minutos: int, descricao: str = "", token: str = None) -> Tuple[bool, Dict[str, Any]]:
    """Cria um novo serviço para o prestador autenticado."""
    payload = {
        "prestador_id": str(prestador_id),
        "titulo": titulo,
        "descricao": descricao,
        "preco": float(preco),
        "duracao_minutos": int(duracao_minutos)
    }
    success, data, status = api_client.post("services", json_data=payload, token=token)
    
    if not success and (status in (404, 500, 502, 503) or (isinstance(data, dict) and data.get("mock_fallback")) or status == 0):
        global _mock_id_counter
        new_service = {
            "id": _mock_id_counter,
            "ativo": True,
            **payload
        }
        MOCK_SERVICES.append(new_service)
        _mock_id_counter += 1
        return True, new_service
        
    if success:
        return True, data
    return False, data

def toggle_service_status(service_id: int, ativo: bool, token: str = None) -> Tuple[bool, Dict[str, Any]]:
    """Ativa ou desativa um serviço."""
    service_id_str = str(service_id)
    success, data, status = api_client.post(f"services/{service_id_str}/toggle", json_data={"ativo": bool(ativo)}, token=token)
    
    if not success and (status in (404, 500, 502, 503) or (isinstance(data, dict) and data.get("mock_fallback")) or status == 0):
        for s in MOCK_SERVICES:
            if str(s["id"]) == service_id_str:
                s["ativo"] = bool(ativo)
                return True, s
        return False, {"message": "Serviço não encontrado no mock."}

    if success:
        return True, data
    return False, data

def get_public_services(token: str = None) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna a lista de serviços ativos disponíveis para visualização pública e de clientes."""
    success, data, status = api_client.get("services", token=token)
    if not success and (status in (404, 500, 502, 503) or (isinstance(data, dict) and data.get("mock_fallback")) or status == 0):
        return True, [s for s in MOCK_SERVICES if s.get("ativo", True)]
    if success:
        items = data if isinstance(data, list) else data.get("items", [])
        return True, [s for s in items if s.get("ativo", True)]
    return False, []
