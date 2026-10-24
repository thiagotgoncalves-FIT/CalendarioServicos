"""
Módulo de serviço para gerenciamento do motor de agendamentos, cálculo de slots livres
e ciclo de vida das reservas (AgendAí).
"""

from datetime import datetime, date, time, timedelta
from typing import List, Dict, Any, Tuple, Optional
from . import api_client
from . import availability_service
from . import catalog_service

# Repositório de fallback em memória para execução resiliente
MOCK_APPOINTMENTS: List[Dict[str, Any]] = []
_mock_appointment_id_counter = 1


def _parse_time(time_str: str) -> Optional[time]:
    """Converte string 'HH:MM' em objeto time."""
    if not time_str:
        return None
    try:
        parts = time_str.strip().split(":")
        return time(int(parts[0]), int(parts[1]))
    except Exception:
        return None


def calculate_available_slots(
    prestador_id: int,
    date_str: str,
    duration_minutes: int,
    token: Optional[str] = None
) -> List[str]:
    """
    Calcula os horários de início disponíveis com passo fixo de 30 minutos.
    Leva em conta:
    1. Grade semanal do prestador (expediente e almoço/pausa).
    2. Horários já agendados (status 'confirmado' ou 'pendente').
    3. Horários passados caso a data consultada seja hoje.
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return []

    # 0 = Domingo, 1 = Segunda ... 6 = Sábado
    dia_semana = int(target_date.strftime("%w"))

    # Busca a grade de horários do prestador
    suc_grade, grade = availability_service.get_availability(prestador_id, token)
    if not suc_grade or not grade:
        return []

    dia_config = next((d for d in grade if d.get("dia_semana") == dia_semana), None)
    if not dia_config or not dia_config.get("ativo"):
        return []

    t_inicio = _parse_time(dia_config.get("hora_inicio"))
    t_fim = _parse_time(dia_config.get("hora_fim"))
    if not t_inicio or not t_fim or t_inicio >= t_fim:
        return []

    t_alm_ini = _parse_time(dia_config.get("intervalo_inicio"))
    t_alm_fim = _parse_time(dia_config.get("intervalo_fim"))
    has_almoco = (t_alm_ini is not None and t_alm_fim is not None and t_alm_ini < t_alm_fim)

    # Busca agendamentos ativos na data para o prestador
    _, appointments = get_appointments_by_date(prestador_id, date_str, token)
    busy_intervals = []
    for app in appointments:
        if app.get("status") in ("confirmado", "pendente"):
            app_start = _parse_time(app.get("hora_inicio"))
            app_dur = app.get("duracao_minutos", 30)
            if app_start:
                app_dt_start = datetime.combine(target_date, app_start)
                app_dt_end = app_dt_start + timedelta(minutes=app_dur)
                busy_intervals.append((app_dt_start, app_dt_end))

    # Geração dos slots candidatos a cada 30 minutos
    slots_disponiveis: List[str] = []
    current_dt = datetime.combine(target_date, t_inicio)
    end_dt = datetime.combine(target_date, t_fim)
    now = datetime.now()

    while current_dt + timedelta(minutes=duration_minutes) <= end_dt:
        slot_start = current_dt
        slot_end = current_dt + timedelta(minutes=duration_minutes)

        # 1. Se a data for hoje, não permite horários passados
        if target_date == date.today() and slot_start <= now:
            current_dt += timedelta(minutes=30)
            continue

        # 2. Verifica colisão com intervalo de almoço
        colide_almoco = False
        if has_almoco:
            alm_start_dt = datetime.combine(target_date, t_alm_ini)
            alm_end_dt = datetime.combine(target_date, t_alm_fim)
            if max(slot_start, alm_start_dt) < min(slot_end, alm_end_dt):
                colide_almoco = True

        if colide_almoco:
            current_dt += timedelta(minutes=30)
            continue

        # 3. Verifica colisão com outros agendamentos (Anti-Double-Booking)
        colide_agendamento = False
        for b_start, b_end in busy_intervals:
            if max(slot_start, b_start) < min(slot_end, b_end):
                colide_agendamento = True
                break

        if not colide_agendamento:
            slots_disponiveis.append(slot_start.strftime("%H:%M"))

        current_dt += timedelta(minutes=30)

    return slots_disponiveis


def get_appointments_by_date(
    prestador_id: int,
    date_str: str,
    token: Optional[str] = None
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna os agendamentos de um prestador em uma data específica."""
    success, data, status = api_client.get(
        "appointments",
        params={"prestador_id": prestador_id, "data": date_str},
        token=token
    )
    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        filtered = [
            a for a in MOCK_APPOINTMENTS
            if a["prestador_id"] == prestador_id and a["data"] == date_str
        ]
        return True, filtered

    if success:
        items = data if isinstance(data, list) else data.get("items", [])
        return True, items
    return False, []


def get_appointments_by_user(
    user_id: int,
    role: str,
    token: Optional[str] = None
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna a lista de agendamentos associados ao usuário autenticado (prestador ou cliente)."""
    success, data, status = api_client.get(
        "appointments",
        params={"user_id": user_id, "role": role},
        token=token
    )
    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        if role == "prestador":
            res = [a for a in MOCK_APPOINTMENTS if a["prestador_id"] == user_id]
        else:
            res = [a for a in MOCK_APPOINTMENTS if a["cliente_id"] == user_id]
        res.sort(key=lambda x: (x.get("data", ""), x.get("hora_inicio", "")))
        return True, res

    if success:
        items = data if isinstance(data, list) else data.get("items", [])
        items.sort(key=lambda x: (x.get("data", ""), x.get("hora_inicio", "")))
        return True, items
    return False, []


def create_appointment(
    cliente_id: int,
    prestador_id: int,
    servico_id: int,
    data_str: str,
    hora_inicio: str,
    token: Optional[str] = None,
    cliente_nome: Optional[str] = None,
    cliente_telefone: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Cria um novo agendamento com validação atômica anti-double-booking.
    """
    # Busca dados do serviço para obter título, preço e duração
    suc_cat, servicos = catalog_service.get_services(prestador_id, token=token)
    if not suc_cat or not servicos:
        suc_cat, servicos = catalog_service.get_public_services(token=token)

    servico = next((s for s in servicos if s.get("id") == servico_id), None)
    if not servico:
        return False, {"message": "Serviço não encontrado no catálogo."}

    duracao = servico.get("duracao_minutos", 30)
    preco = servico.get("preco", 0.0)
    titulo = servico.get("titulo", "Serviço")

    # Validação anti-double-booking reconfirmando se o horário está livre
    slots = calculate_available_slots(prestador_id, data_str, duracao, token=token)
    if hora_inicio not in slots:
        return False, {"message": "O horário selecionado não está mais disponível. Por favor, escolha outro slot."}

    payload = {
        "cliente_id": cliente_id,
        "prestador_id": prestador_id,
        "servico_id": servico_id,
        "servico_titulo": titulo,
        "data": data_str,
        "hora_inicio": hora_inicio,
        "duracao_minutos": duracao,
        "valor_cobrado": preco,
        "status": "confirmado",
        "cliente_nome": cliente_nome or "",
        "cliente_telefone": cliente_telefone or ""
    }

    success, data, status = api_client.post("appointments", json_data=payload, token=token)

    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        global _mock_appointment_id_counter
        new_app = {
            "id": _mock_appointment_id_counter,
            "cliente_id": cliente_id,
            "cliente_nome": cliente_nome or f"Cliente #{cliente_id}",
            "cliente_telefone": cliente_telefone or "",
            "prestador_id": prestador_id,
            "servico_id": servico_id,
            "servico_titulo": titulo,
            "data": data_str,
            "hora_inicio": hora_inicio,
            "duracao_minutos": duracao,
            "valor_cobrado": preco,
            "status": "confirmado",
            "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        MOCK_APPOINTMENTS.append(new_app)
        _mock_appointment_id_counter += 1
        return True, new_app

    if success:
        return True, data
    return False, data


def update_appointment_status(
    appointment_id: int,
    new_status: str,
    token: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Atualiza o status de um agendamento ('confirmado', 'concluido', 'cancelado').
    """
    status_validos = ("pendente", "confirmado", "concluido", "cancelado")
    if new_status not in status_validos:
        return False, {"message": f"Status '{new_status}' inválido."}

    success, data, status = api_client.post(
        f"appointments/{appointment_id}/status",
        json_data={"status": new_status},
        token=token
    )

    if not success and (status in (404, 503) or (isinstance(data, dict) and data.get("mock_fallback"))):
        for app in MOCK_APPOINTMENTS:
            if app["id"] == appointment_id:
                app["status"] = new_status
                return True, app
        return False, {"message": "Agendamento não encontrado no mock."}

    if success:
        return True, data
    return False, data
