"""
Módulo de serviço para gerenciamento da grade de disponibilidade do prestador.
"""
from typing import List, Dict, Any, Tuple
from . import api_client

# Dados mockados
MOCK_AVAILABILITY = {
    1: [
        {"dia_semana": 1, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": True},
        {"dia_semana": 2, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": True},
        {"dia_semana": 3, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": True},
        {"dia_semana": 4, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": True},
        {"dia_semana": 5, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": True},
        {"dia_semana": 6, "hora_inicio": "09:00", "hora_fim": "14:00", "intervalo_inicio": None, "intervalo_fim": None, "ativo": True},
        {"dia_semana": 0, "hora_inicio": "00:00", "hora_fim": "00:00", "intervalo_inicio": None, "intervalo_fim": None, "ativo": False},
    ]
}

def get_availability(prestador_id: int, token: str = None) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna a configuração dos 7 dias da semana do prestador."""
    success, data, status = api_client.get("availability", params={"prestador_id": prestador_id}, token=token)
    
    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        return True, MOCK_AVAILABILITY.get(prestador_id, [])
    
    if success:
        return True, data if isinstance(data, list) else data.get("items", [])
    return False, []

def save_availability(prestador_id: int, schedule_data: List[Dict[str, Any]], token: str = None) -> Tuple[bool, Any]:
    """Salva a grade de horários semanal do prestador."""
    success, data, status = api_client.post("availability", json_data={"schedule": schedule_data}, token=token)
    
    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        MOCK_AVAILABILITY[prestador_id] = schedule_data
        return True, {"message": "Disponibilidade salva com sucesso (mock)."}
    
    if success:
        return True, data
    return False, data
