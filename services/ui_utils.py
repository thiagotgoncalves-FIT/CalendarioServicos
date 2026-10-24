"""
Utilitários de UI e formatação para padrão brasileiro (pt-BR).
"""

from datetime import date, datetime
from typing import Union, Optional

MESES_PT_BR = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

DIAS_SEMANA_PT_BR = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

def format_currency_brl(val: Union[int, float, str, None]) -> str:
    """Formata valor numérico para padrão monetário brasileiro R$ 0,00."""
    if val is None:
        return "R$ 0,00"
    try:
        num = float(val)
        formatted = f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"
    except (ValueError, TypeError):
        return "R$ 0,00"

def format_date_long_pt_br(d: Optional[date] = None) -> str:
    """Retorna data formatada por extenso, ex: '18 de outubro de 2026'."""
    if d is None:
        d = date.today()
    mes = MESES_PT_BR.get(d.month, "")
    return f"{d.day} de {mes} de {d.year}"

def format_date_short_pt_br(d_str: Union[str, date, None]) -> str:
    """Converte 'YYYY-MM-DD' para 'DD/MM/YYYY'."""
    if not d_str:
        return ""
    if isinstance(d_str, (date, datetime)):
        return d_str.strftime("%d/%m/%Y")
    try:
        parts = str(d_str).split("-")
        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
    except Exception:
        pass
    return str(d_str)

def get_initials(name: Optional[str]) -> str:
    """Extrai as iniciais do nome, ex: 'Hector Barros' -> 'HB'."""
    if not name or not name.strip():
        return "AG"
    parts = name.strip().split()
    if len(parts) == 1:
        return parts[0][:2].upper()
    return f"{parts[0][0]}{parts[-1][0]}".upper()

def status_badge_html(status: str) -> str:
    """Retorna badge HTML estilizado para o status do agendamento."""
    status_lower = (status or "").lower()
    badges = {
        "confirmado": ('#10B981', 'rgba(16, 185, 129, 0.15)', 'rgba(16, 185, 129, 0.3)', 'Confirmado'),
        "concluido": ('#3B82F6', 'rgba(59, 130, 246, 0.15)', 'rgba(59, 130, 246, 0.3)', 'Concluído'),
        "pendente": ('#F59E0B', 'rgba(245, 158, 11, 0.15)', 'rgba(245, 158, 11, 0.3)', 'Pendente'),
        "cancelado": ('#EF4444', 'rgba(239, 68, 68, 0.15)', 'rgba(239, 68, 68, 0.3)', 'Cancelado')
    }
    color, bg, border, label = badges.get(status_lower, ('#94A3B8', 'rgba(148, 163, 184, 0.15)', 'rgba(148, 163, 184, 0.3)', status.capitalize()))
    return f'<span style="display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; color:{color}; background:{bg}; border:1px solid {border};">{label}</span>'

def metric_card_html(title: str, value: str, subtitle: str, icon: str = "") -> str:
    """Retorna card de métrica neutro com design dark moderno e sem setas enganosas."""
    return f"""
    <div style="background:#111827; border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:1.25rem 1.5rem; box-shadow:0 4px 16px rgba(0,0,0,0.25);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span style="font-size:0.85rem; font-weight:600; color:#94A3B8; text-transform:uppercase; letter-spacing:0.04em;">{title}</span>
            <span style="font-size:1.25rem;">{icon}</span>
        </div>
        <div style="font-size:2rem; font-weight:800; color:#F8FAFC; line-height:1.2; margin-bottom:0.35rem;">{value}</div>
        <div style="font-size:0.8rem; color:#64748B;">{subtitle}</div>
    </div>
    """

def empty_state_html(icon: str, title: str, description: str) -> str:
    """Renderiza container de estado vazio amigável e profissional."""
    return f"""
    <div style="text-align:center; padding:3rem 1.5rem; background:#111827; border-radius:14px; border:1px dashed rgba(255,255,255,0.12); margin:1.5rem 0;">
        <div style="font-size:2.8rem; margin-bottom:0.75rem;">{icon}</div>
        <div style="font-size:1.15rem; font-weight:700; color:#F1F5F9; margin-bottom:0.4rem;">{title}</div>
        <div style="font-size:0.9rem; color:#94A3B8; max-width:440px; margin:0 auto; line-height:1.5;">{description}</div>
    </div>
    """

import csv
import io
import re
import urllib.parse
from typing import List, Dict, Any

def generate_appointments_csv(atendimentos: List[Dict[str, Any]]) -> str:
    """
    Gera conteúdo CSV em memória formatado em pt-BR (UTF-8 com BOM).
    Cabeçalhos: ID, Data, Horário, Serviço, Duração (min), Valor Cobrado, Status, ID Cliente.
    """
    output = io.StringIO()
    output.write("\ufeff")  # BOM para compatibilidade com Excel em português
    writer = csv.writer(output, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    
    writer.writerow([
        "ID",
        "Data",
        "Horário",
        "Serviço",
        "Duração (min)",
        "Valor Cobrado",
        "Status",
        "ID Cliente"
    ])
    
    for a in (atendimentos or []):
        data_fmt = format_date_short_pt_br(a.get("data"))
        valor_fmt = format_currency_brl(a.get("valor_cobrado", 0))
        writer.writerow([
            a.get("id", ""),
            data_fmt,
            a.get("hora_inicio", ""),
            a.get("servico_titulo", "Serviço"),
            a.get("duracao_minutos", 30),
            valor_fmt,
            str(a.get("status") or "").capitalize(),
            a.get("cliente_id", "")
        ])
        
    return output.getvalue()

def get_whatsapp_link(
    phone: Optional[str],
    cliente_nome: Optional[str] = None,
    servico_titulo: Optional[str] = None,
    data_str: Optional[str] = None,
    hora_str: Optional[str] = None
) -> Optional[str]:
    """
    Gera link universal do WhatsApp (https://wa.me/55...) com mensagem pré-formatada.
    Sanitiza caracteres não-numéricos e valida formato brasileiro.
    """
    if not phone:
        return None
    digits = re.sub(r"\D", "", str(phone))
    if not digits:
        return None
    if len(digits) in (10, 11):
        digits = f"55{digits}"
    elif len(digits) < 10:
        return None
    
    nome = cliente_nome or "Cliente"
    servico = servico_titulo or "atendimento"
    data_fmt = format_date_short_pt_br(data_str) if data_str else "sua data"
    hora = hora_str or "horário agendado"
    
    msg = (
        f"Olá {nome}! 👋 Confirmando seu agendamento de {servico} "
        f"no AgendAí para {data_fmt} às {hora}. Qualquer dúvida estou à disposição!"
    )
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{digits}?text={encoded_msg}"

