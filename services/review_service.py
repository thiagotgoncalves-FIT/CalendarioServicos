"""
Módulo de serviço para gerenciamento do sistema de avaliações e reputação (AgendAí).
Suporta submissão de avaliações pós-atendimento vinculadas a serviços, regras estritas de elegibilidade,
cálculo de métricas contextuais por serviço e camada de resiliência.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional, Union
from . import api_client
from . import appointment_service
from .ui_utils import normalize_status

# Caminhos de persistência durável local
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
REVIEWS_FILE = os.path.join(UPLOAD_DIR, "reviews.json")
REVIEWED_APPS_FILE = os.path.join(UPLOAD_DIR, "reviewed_appointments.json")

# Repositório inicial de fallback em memória para execução resiliente
DEFAULT_REVIEWS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "agendamento_id": "991",
        "cliente_id": "101",
        "prestador_id": "15",
        "servico_id": "1",
        "servico_titulo": "Corte Masculino & Barba",
        "cliente_nome_exibicao": "Camila R.",
        "nota": 5,
        "comentario": "Excelente atendimento! O profissional foi super pontual e o corte ficou impecável. Recomendo muito!",
        "criado_em": "2026-10-28 14:30:00"
    },
    {
        "id": 2,
        "agendamento_id": "992",
        "cliente_id": "102",
        "prestador_id": "15",
        "servico_id": "1",
        "servico_titulo": "Corte Masculino & Barba",
        "cliente_nome_exibicao": "Rodrigo M.",
        "nota": 5,
        "comentario": "Espaço muito bem organizado e profissional atencioso. Agendamento prático e sem espera.",
        "criado_em": "2026-10-30 11:15:00"
    },
    {
        "id": 3,
        "agendamento_id": "993",
        "cliente_id": "103",
        "prestador_id": "15",
        "servico_id": "1",
        "servico_titulo": "Corte Masculino & Barba",
        "cliente_nome_exibicao": "Juliana S.",
        "nota": 4,
        "comentario": "Gostei bastante do resultado do serviço. Agilidade no agendamento pelo site e ótimo atendimento.",
        "criado_em": "2026-11-02 16:45:00"
    }
]

MOCK_REVIEWS: List[Dict[str, Any]] = []
_mock_review_id_counter = 4


def _ensure_upload_dir() -> None:
    """Garante que a pasta de uploads exista."""
    if not os.path.exists(UPLOAD_DIR):
        try:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
        except Exception:
            pass


def _load_persisted_reviews() -> List[Dict[str, Any]]:
    """Carrega avaliações persistidas do arquivo JSON ou inicializa com DEFAULT_REVIEWS."""
    _ensure_upload_dir()
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    # Se não existir ou falhar, inicializa com cópia dos default e grava
    initial = [dict(r) for r in DEFAULT_REVIEWS]
    _save_persisted_reviews(initial)
    return initial


def _save_persisted_reviews(reviews: List[Dict[str, Any]]) -> None:
    """Salva a lista de avaliações no arquivo JSON de forma durável."""
    _ensure_upload_dir()
    try:
        with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _load_reviewed_appointments() -> List[str]:
    """Carrega a lista de IDs de agendamentos avaliados persistidos."""
    _ensure_upload_dir()
    if os.path.exists(REVIEWED_APPS_FILE):
        try:
            with open(REVIEWED_APPS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [str(x) for x in data]
        except Exception:
            pass
    # Por padrão, agendamentos iniciais 991, 992, 993 já constam como avaliados
    initial = ["991", "992", "993"]
    _save_reviewed_appointments(initial)
    return initial


def _save_reviewed_appointments(app_ids: List[str]) -> None:
    """Salva a lista de agendamentos avaliados no arquivo JSON."""
    _ensure_upload_dir()
    try:
        with open(REVIEWED_APPS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(set(str(x) for x in app_ids)), f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def mark_appointment_persisted_reviewed(agendamento_id: Union[int, str]) -> None:
    """Registra duravelmente o ID do agendamento como avaliado."""
    app_id_str = str(agendamento_id)
    current = _load_reviewed_appointments()
    if app_id_str not in current:
        current.append(app_id_str)
        _save_reviewed_appointments(current)


# Inicializa cache em memória MOCK_REVIEWS a partir do arquivo persistido
MOCK_REVIEWS = _load_persisted_reviews()
if MOCK_REVIEWS:
    max_id = max([int(r.get("id", 0)) for r in MOCK_REVIEWS if str(r.get("id", "")).isdigit()] or [3])
    _mock_review_id_counter = max_id + 1


def migrate_legacy_reviews() -> None:
    """Garante retrocompatibilidade preenchendo servico_id e servico_titulo em avaliações existentes."""
    for r in MOCK_REVIEWS:
        if not r.get("servico_id"):
            app_id = r.get("agendamento_id")
            app = appointment_service.get_appointment_by_id(app_id) if app_id else None
            if app and app.get("servico_id"):
                r["servico_id"] = app.get("servico_id")
                r["servico_titulo"] = app.get("servico_titulo", "Serviço Especializado")
            else:
                r["servico_id"] = 1
                r["servico_titulo"] = "Corte Masculino & Barba"


# Executa migração na inicialização
migrate_legacy_reviews()


def format_client_name(full_name: Optional[str]) -> str:
    """
    Formata o nome do cliente para exibição pública com privacidade.
    Ex: 'Lucas Ferreira' -> 'Lucas F.', 'Mariana Silva Santos' -> 'Mariana S.'
    """
    if not full_name or not full_name.strip():
        return "Cliente"
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0].capitalize()
    return f"{parts[0].capitalize()} {parts[-1][0].upper()}."


def validate_review_input(nota: Any, comentario: Optional[str]) -> Tuple[bool, str]:
    """Valida os parâmetros de submissão de uma avaliação."""
    try:
        nota_int = int(nota)
    except (ValueError, TypeError):
        return False, "A nota deve ser um número inteiro entre 1 e 5."

    if nota_int < 1 or nota_int > 5:
        return False, "A nota deve estar entre 1 e 5 estrelas."

    texto = (comentario or "").strip()
    if len(texto) > 500:
        return False, "O comentário deve ter no máximo 500 caracteres."

    return True, ""


def is_appointment_reviewed(agendamento_id: Union[int, str], token: Optional[str] = None) -> bool:
    """Verifica se um agendamento já foi previamente avaliado comparando IDs textualmente."""
    agendamento_id_str = str(agendamento_id)

    # 1. Checa agendamentos avaliados persistidos em disco
    reviewed_ids = _load_reviewed_appointments()
    if agendamento_id_str in reviewed_ids:
        return True

    # 2. Checa avaliações carregadas / persistidas
    current_reviews = _load_persisted_reviews()
    for r in current_reviews:
        if str(r.get("agendamento_id")) == agendamento_id_str:
            mark_appointment_persisted_reviewed(agendamento_id_str)
            return True

    # 3. Consulta API remota se disponível
    success, data, status = api_client.get(f"reviews/appointment/{agendamento_id_str}", token=token)
    if success and data:
        mark_appointment_persisted_reviewed(agendamento_id_str)
        return True
    return False


def get_review_by_appointment(agendamento_id: Union[int, str], token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retorna a avaliação associada a um agendamento, se houver."""
    agendamento_id_str = str(agendamento_id)
    current_reviews = _load_persisted_reviews()
    for r in current_reviews:
        if str(r.get("agendamento_id")) == agendamento_id_str:
            return r

    success, data, status = api_client.get(f"reviews/appointment/{agendamento_id_str}", token=token)
    if success and isinstance(data, dict):
        return data
    return None


def submit_review(
    agendamento_id: Union[int, str],
    cliente_id: Union[int, str],
    prestador_id: Union[int, str],
    nota: Any,
    comentario: str,
    cliente_nome: str,
    servico_id: Optional[Union[int, str]] = None,
    servico_titulo: Optional[str] = None,
    token: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Submete uma nova avaliação herdando o serviço a partir do agendamento concluído.
    Valida elegibilidade (somente titular e atendimento concluído), unicidade e notas de 1 a 5.
    Compara IDs estritamente como texto: str(a) == str(b).
    """
    valido, msg_erro = validate_review_input(nota, comentario)
    if not valido:
        return False, {"message": msg_erro}

    # Validação de unicidade
    if is_appointment_reviewed(agendamento_id, token=token):
        return False, {"message": "Este atendimento já foi avaliado anteriormente."}

    # Validação de elegibilidade com o agendamento e herança do serviço
    app = appointment_service.get_appointment_by_id(agendamento_id, token=token)
    resolved_servico_id = servico_id
    resolved_servico_titulo = servico_titulo

    if app:
        st_app = normalize_status(app.get("status"))
        if st_app != "concluido":
            return False, {"message": "Apenas atendimentos marcados como concluídos podem ser avaliados."}
        if app.get("cliente_id") is not None and str(app.get("cliente_id")) != str(cliente_id):
            return False, {"message": "Apenas o cliente titular do atendimento pode avaliá-lo."}
        resolved_servico_id = app.get("servico_id", resolved_servico_id or 1)
        resolved_servico_titulo = app.get("servico_titulo", resolved_servico_titulo or "Serviço")

    if not resolved_servico_id:
        resolved_servico_id = 1
        resolved_servico_titulo = "Corte Masculino & Barba"

    nome_exib = format_client_name(cliente_nome)
    comentario_limpo = (comentario or "").strip()

    payload = {
        "agendamento_id": str(agendamento_id),
        "cliente_id": str(cliente_id),
        "prestador_id": str(prestador_id),
        "servico_id": str(resolved_servico_id),
        "servico_titulo": resolved_servico_titulo,
        "nota": int(nota),
        "comentario": comentario_limpo,
        "cliente_nome_exibicao": nome_exib,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    success, data, status = api_client.post("reviews", json_data=payload, token=token)

    # Registra duravelmente o atendimento como avaliado no disco
    mark_appointment_persisted_reviewed(agendamento_id)

    # Se a gravação no Xano falhar ou estiver em fallback, garante a persistência no repositório local sem perda
    if not success:
        global _mock_review_id_counter
        review_obj = {
            "id": _mock_review_id_counter,
            **payload
        }
        # Previne duplicata caso já exista
        current_revs = _load_persisted_reviews()
        if not any(str(r.get("agendamento_id")) == str(agendamento_id) for r in current_revs):
            current_revs.insert(0, review_obj)
            _save_persisted_reviews(current_revs)
            MOCK_REVIEWS.clear()
            MOCK_REVIEWS.extend(current_revs)
            _mock_review_id_counter += 1

        # Marca o agendamento no mock como avaliado
        appointment_service.mark_appointment_reviewed(agendamento_id)
        return True, review_obj

    if success:
        # Mantém também no cache local e em disco para leitura coerente imediata
        saved_obj = data if isinstance(data, dict) else payload
        current_revs = _load_persisted_reviews()
        if not any(str(r.get("agendamento_id")) == str(agendamento_id) for r in current_revs):
            current_revs.insert(0, saved_obj)
            _save_persisted_reviews(current_revs)
            MOCK_REVIEWS.clear()
            MOCK_REVIEWS.extend(current_revs)
        appointment_service.mark_appointment_reviewed(agendamento_id)
        return True, saved_obj
    return False, data


def get_reviews(
    prestador_id: Optional[Union[int, str]] = None,
    servico_id: Optional[Union[int, str]] = None,
    token: Optional[str] = None,
    *args,
    **kwargs
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Retorna avaliações cadastradas filtradas opcionalmente por prestador e/ou serviço."""
    migrate_legacy_reviews()
    if servico_id is None and "servico_id" in kwargs:
        servico_id = kwargs["servico_id"]
    if prestador_id is None and "prestador_id" in kwargs:
        prestador_id = kwargs["prestador_id"]
    if token is None and "token" in kwargs:
        token = kwargs["token"]

    params = {}
    if prestador_id is not None:
        params["prestador_id"] = str(prestador_id)
    if servico_id is not None:
        params["servico_id"] = str(servico_id)

    success, data, status = api_client.get("reviews", params=params, token=token)
    if not success:
        itens = _load_persisted_reviews()
        if prestador_id is not None:
            itens = [r for r in itens if str(r.get("prestador_id")) == str(prestador_id)]
        if servico_id is not None:
            itens = [r for r in itens if str(r.get("servico_id")) == str(servico_id)]
        itens.sort(key=lambda r: r.get("criado_em", ""), reverse=True)
        return True, itens

    if success:
        itens = data if isinstance(data, list) else data.get("items", [])
        # Caso a API retorne vazio ou lista parcial, mescla com avaliações locais salvas
        local_itens = _load_persisted_reviews()
        known_ids = {str(r.get("agendamento_id")) for r in itens if r.get("agendamento_id")}
        for loc in local_itens:
            if str(loc.get("agendamento_id")) not in known_ids:
                itens.append(loc)

        if servico_id is not None:
            itens = [r for r in itens if str(r.get("servico_id")) == str(servico_id)]
        itens.sort(key=lambda r: r.get("criado_em", ""), reverse=True)
        return True, itens

    return False, []


def get_metrics(
    prestador_id: Optional[int] = None,
    servico_id: Optional[int] = None,
    token: Optional[str] = None,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """Calcula métricas consolidadas (nota média e total de avaliações) por prestador ou serviço."""
    if servico_id is None and "servico_id" in kwargs:
        servico_id = kwargs["servico_id"]
    if prestador_id is None and "prestador_id" in kwargs:
        prestador_id = kwargs["prestador_id"]
    if token is None and "token" in kwargs:
        token = kwargs["token"]

    _, reviews = get_reviews(prestador_id=prestador_id, servico_id=servico_id, token=token)
    if not reviews:
        return {"nota_media": 0.0, "total_avaliacoes": 0}

    total = len(reviews)
    soma_notas = sum(float(r.get("nota", 0)) for r in reviews)
    media = round(soma_notas / total, 1) if total > 0 else 0.0

    return {
        "nota_media": media,
        "total_avaliacoes": total
    }


def format_service_reviews_label(servico_id: int, token: Optional[str] = None) -> str:
    """Retorna o rótulo descritivo para o botão ou resumo de avaliações do serviço."""
    m = get_metrics(servico_id=servico_id, token=token)
    total = m.get("total_avaliacoes", 0)
    if total == 0:
        return "Avaliações (Novo)"
    media_str = f"{m.get('nota_media', 0.0):.1f}".replace(".", ",")
    return f"Avaliações ({media_str} ★ · {total})"
