"""
Utilitários de UI e formatação para padrão brasileiro (pt-BR).
"""

from datetime import date, datetime
from typing import Union, Optional, Dict, Any
import base64
import os
import unicodedata
from pathlib import Path


def normalize_status(status: Optional[str]) -> str:
    """
    Normaliza status de agendamento usando unicodedata:
    remove acentuação gráfica, espaços extras e converte para minúsculas.
    Ex: 'Concluído' -> 'concluido', 'PENDENTE ' -> 'pendente'.
    """
    if not status:
        return ""
    texto = str(status).strip()
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.lower()


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


def status_badge_html(status: Optional[str]) -> str:
    """Retorna badge HTML estilizado para o status do agendamento com destaque em negrito e visual cartoon."""
    st_norm = normalize_status(status)
    badges = {
        "confirmado": ('#047857', '#ECFDF5', '#A7F3D0', 'Confirmado'),
        "concluido": ('#1D4ED8', '#EFF6FF', '#BFDBFE', 'Concluído'),
        "pendente": ('#B45309', '#FFFBEB', '#FDE68A', 'Pendente'),
        "cancelado": ('#B91C1C', '#FEF2F2', '#FECACA', 'Cancelado')
    }
    color, bg, border, label = badges.get(st_norm, ('#475569', '#F1F5F9', '#CBD5E1', (status or '').capitalize()))
    return f'<span style="display:inline-block; padding:5px 14px; border-radius:20px; font-size:0.82rem; font-weight:800; text-transform:uppercase; letter-spacing:0.4px; color:{color}; background:{bg}; border:1.5px solid {border};">{label}</span>'

def metric_card_html(title: str, value: str, subtitle: str, icon: str = "") -> str:
    """Retorna card de métrica neutro com design limpo em cinza claro e azul."""
    icon_span = f'<span style="font-size:1.25rem;">{icon}</span>' if icon else ""
    return (
        f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.25rem 1.5rem; box-shadow:0 1px 4px rgba(0,0,0,0.05);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">'
        f'<span style="font-size:0.85rem; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">{title}</span>'
        f'{icon_span}'
        f'</div>'
        f'<div style="font-size:2rem; font-weight:800; color:#0F172A; line-height:1.2; margin-bottom:0.35rem;">{value}</div>'
        f'<div style="font-size:0.8rem; color:#64748B;">{subtitle}</div>'
        f'</div>'
    )

def empty_state_html(icon: str, title: str, description: str) -> str:
    """Renderiza container de estado vazio amigável e profissional em tema claro."""
    icon_span = f'<div style="font-size:2.8rem; margin-bottom:0.75rem;">{icon}</div>' if icon else ""
    return (
        f'<div style="text-align:center; padding:3rem 1.5rem; background:#FFFFFF; border-radius:14px; border:1px dashed #CBD5E1; margin:1.5rem 0; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
        f'{icon_span}'
        f'<div style="font-size:1.15rem; font-weight:700; color:#0F172A; margin-bottom:0.4rem;">{title}</div>'
        f'<div style="font-size:0.9rem; color:#64748B; max-width:440px; margin:0 auto; line-height:1.5;">{description}</div>'
        f'</div>'
    )

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
        f"Olá {nome}! Confirmando seu agendamento de {servico} "
        f"no AgendAí para {data_fmt} às {hora}. Qualquer dúvida estou à disposição!"
    )
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{digits}?text={encoded_msg}"

def section_header_html(title: str, subtitle: str, icon: str = "") -> str:
    """Renderiza cabeçalho de seção com hierarquia visual moderna em tema claro."""
    icon_span = f'<span style="font-size:1.6rem; margin-right:0.6rem;">{icon}</span>' if icon else ""
    return (
        f'<div style="margin-bottom:1.5rem; border-bottom:1px solid #E2E8F0; padding-bottom:0.75rem;">'
        f'<div style="display:flex; align-items:center;">'
        f'{icon_span}'
        f'<h2 style="font-size:1.4rem; font-weight:700; color:#0F172A; margin:0; letter-spacing:-0.02em;">{title}</h2>'
        f'</div>'
        f'<p style="font-size:0.9rem; color:#64748B; margin-top:0.3rem; margin-bottom:0; line-height:1.4;">{subtitle}</p>'
        f'</div>'
    )

def recommendation_badge_html(score: float) -> str:
    """Badge de pontuação (Score) do algoritmo de recomendação em tema claro."""
    if score >= 85:
        bg = "#ECFDF5"
        border = "#A7F3D0"
        color = "#047857"
        label = "Excelente Match"
    elif score >= 70:
        bg = "#EFF6FF"
        border = "#BFDBFE"
        color = "#1D4ED8"
        label = "Recomendado"
    else:
        bg = "#FFFBEB"
        border = "#FDE68A"
        color = "#B45309"
        label = "Compatível"

    return (
        f'<div style="display:inline-flex; align-items:center; gap:6px; background:{bg}; border:1px solid {border}; border-radius:20px; padding:4px 12px;">'
        f'<span style="font-size:0.9rem; font-weight:800; color:{color};">{score:.0f}/100</span>'
        f'<span style="font-size:0.75rem; font-weight:600; color:#334155;">• {label}</span>'
        f'</div>'
    )


def render_stars_html(rating: Union[int, float], max_stars: int = 5) -> str:
    """Renderiza estrelas douradas em HTML para visualização de notas."""
    try:
        r = float(rating)
    except (ValueError, TypeError):
        r = 0.0
    full_stars = min(max_stars, max(0, int(round(r))))
    empty_stars = max(0, max_stars - full_stars)
    stars_str = "★" * full_stars + "☆" * empty_stars
    return (
        f'<span style="color:#F59E0B; font-size:1.15rem; letter-spacing:2px; font-weight:700;">{stars_str}</span>'
        f'<span style="font-size:0.85rem; font-weight:700; color:#475569; margin-left:6px;">{r:.1f}</span>'
    )


def review_card_html(
    nome: str,
    rating: int,
    data_str: str,
    comentario: str,
    servico_titulo: Optional[str] = None
) -> str:
    """Renderiza card individual de avaliação em padrão visual limpo e responsivo com identificação opcional do serviço."""
    stars_html = render_stars_html(rating)
    servico_badge = ""
    if servico_titulo:
        servico_badge = (
            f'<div style="margin-bottom:0.4rem;">'
            f'<span style="display:inline-block; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; color:#1D4ED8; background:#EFF6FF; border:1px solid #BFDBFE;">{servico_titulo}</span>'
            f'</div>'
        )

    return (
        f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.25rem 1.5rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
        f'{servico_badge}'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; flex-wrap:wrap; gap:8px;">'
        f'<div style="font-weight:700; font-size:1rem; color:#0F172A;">{nome}</div>'
        f'<div style="display:flex; align-items:center; gap:10px;">'
        f'{stars_html}'
        f'<span style="font-size:0.8rem; color:#94A3B8;">{data_str}</span>'
        f'</div>'
        f'</div>'
        f'<div style="font-size:0.92rem; color:#334155; line-height:1.5;">{comentario}</div>'
        f'</div>'
    )


def service_reviews_summary_html(nota_media: float, total_avaliacoes: int) -> str:
    """Renderiza cabeçalho de resumo de avaliações de um serviço específico."""
    if total_avaliacoes == 0:
        return (
            '<div style="background:#F8FAFC; border:1px dashed #CBD5E1; border-radius:12px; padding:1rem; margin-bottom:1rem; text-align:center;">'
            '<span style="font-size:0.85rem; font-weight:600; color:#64748B;">Este serviço ainda não possui avaliações.</span>'
            '</div>'
        )
    stars_html = render_stars_html(nota_media)
    plural = "avaliações" if total_avaliacoes != 1 else "avaliação"
    return (
        f'<div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1rem 1.25rem; margin-bottom:1.2rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
        f'<div style="display:flex; align-items:center; gap:8px;">{stars_html}</div>'
        f'<span style="font-size:0.85rem; font-weight:700; color:#334155;">{total_avaliacoes} {plural}</span>'
        f'</div>'
    )


def user_avatar_html(user: Optional[Dict[str, Any]] = None, size: int = 44) -> str:
    """
    Renderiza o avatar circular do usuário:
    - Se houver foto em `photo_url` e o arquivo existir no disco, renderiza imagem circular com recorte centralizado.
    - Caso contrário, renderiza círculo gradiente elegante com as iniciais do nome.
    """
    user = user or {}
    name = user.get("name", "Usuário")
    photo_path = user.get("photo_url")
    
    font_size = max(0.75, round(size * 0.024, 2))
    
    # Se existe caminho e arquivo no disco, converte para base64 data URI
    if photo_path and os.path.exists(photo_path):
        try:
            with open(photo_path, "rb") as img_file:
                b64_data = base64.b64encode(img_file.read()).decode("utf-8")
                ext = os.path.splitext(photo_path)[1].lower().replace(".", "")
                mime = "jpeg" if ext in ("jpg", "jpeg") else ext
                data_uri = f"data:image/{mime};base64,{b64_data}"
                return (
                    f'<div style="width:{size}px; height:{size}px; border-radius:50%; overflow:hidden; '
                    f'box-shadow:0 4px 10px rgba(37,99,235,0.25); border:2px solid #3B82F6; flex-shrink:0;">'
                    f'<img src="{data_uri}" style="width:100%; height:100%; object-fit:cover; display:block;" alt="{name}" />'
                    f'</div>'
                )
        except Exception:
            pass

    # Fallback para iniciais estilizadas
    initials = get_initials(name)
    return (
        f'<div style="width:{size}px; height:{size}px; border-radius:50%; '
        f'background:linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); '
        f'display:flex; align-items:center; justify-content:center; font-weight:800; '
        f'font-size:{font_size}rem; color:#FFFFFF; box-shadow:0 4px 10px rgba(37,99,235,0.25); flex-shrink:0;">'
        f'{initials}</div>'
    )


def apply_theme_and_clean_ui(theme_name: str = "claro") -> str:
    """
    Gera o bloco <style> que injeta as regras de estilo dinâmico para os temas Claro e Escuro,
    além de ocultar elementos técnicos nativos do Streamlit (cabeçalho, rodapé e botões de desenvolvedor).
    """
    theme = (theme_name or "claro").lower().strip()
    is_dark = (theme == "escuro")
    
    # Regras universais de limpeza técnica da interface, tipografia cartoon e abas verticais
    clean_css = """
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700;800&family=Quicksand:wght@500;600;700;800&display=swap');

    /* Tipografia Cartoon & Amigável Universal */
    html, body, [class*="st-"], .stApp, button, input, textarea, select, .stMarkdown {
        font-family: 'Fredoka', 'Quicksand', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        letter-spacing: 0.2px;
    }

    /* Proteção de fontes para ícones nativos do Streamlit (Material Symbols / Icons) */
    [data-testid="stIconMaterial"],
    [data-testid*="Icon"],
    [class*="material-icons"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    span[data-testid="stIconMaterial"],
    i[class*="icon"] {
        font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
        font-weight: normal !important;
        font-style: normal !important;
        display: inline-block !important;
        line-height: 1 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        word-wrap: normal !important;
        white-space: nowrap !important;
        direction: ltr !important;
    }

    /* Destaques importantes em negrito marcante */
    b, strong, .saas-metric-val, [data-testid="stMetricValue"] {
        font-weight: 800 !important;
    }

    /* Remove rodapé e elementos desnecessários sem interferir no controle da sidebar */
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    footer {
        display: none !important;
        visibility: hidden !important;
    }
    button[title="Deploy this app"] {
        display: none !important;
    }
    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* Cabeçalho nativo transparente */
    header[data-testid="stHeader"] {
        background: transparent !important;
        color: inherit !important;
    }

    /* Ocultar e desativar permanentemente os botões de recolhimento da barra lateral */
    button[data-testid="stSidebarCollapseButton"],
    div[data-testid="stSidebarCollapsedControl"],
    div[data-testid="stSidebarCollapsedControl"] button,
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Fixação permanente da barra lateral aberta */
    section[data-testid="stSidebar"],
    div[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        transform: none !important;
        min-width: 300px !important;
        max-width: 320px !important;
        width: 300px !important;
        position: relative !important;
        margin-left: 0 !important;
    }

    /* Barra de navegação e retorno independente no topo da área principal */
    .top-nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0.75rem;
        margin-bottom: 1rem;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .top-nav-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Layout Vertical para Abas (Tabs) do Streamlit */
    .stTabs [data-baseweb="tab-list"],
    div[data-testid="stTabs"] [data-baseweb="tab-list"],
    div[data-baseweb="tab-list"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.6rem !important;
        border-bottom: none !important;
        width: 100% !important;
        max-width: 320px !important;
        margin-bottom: 1.5rem !important;
    }

    /* Oculta a linha de highlight horizontal que quebra no modo vertical */
    [data-baseweb="tab-highlight"] {
        display: none !important;
        visibility: hidden !important;
    }

    .stTabs [data-baseweb="tab"],
    div[data-testid="stTabs"] button[role="tab"] {
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 0.85rem 1.25rem !important;
        border-radius: 14px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        border: 1.5px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        color: #334155 !important;
        margin-bottom: 4px !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stTabs [data-baseweb="tab"]:hover,
    div[data-testid="stTabs"] button[role="tab"]:hover {
        background-color: #F1F5F9 !important;
        border-color: #CBD5E1 !important;
        color: #0F172A !important;
        transform: translateX(3px);
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background-color: #EEF2FF !important;
        border-color: #6366F1 !important;
        color: #4F46E5 !important;
        font-weight: 800 !important;
        box-shadow: 0 3px 10px rgba(99, 102, 241, 0.15) !important;
    }

    div[data-testid="stTabs"] button[role="tab"] > div,
    .stTabs [data-baseweb="tab"] > div {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        width: 100% !important;
        text-align: left !important;
    }
    """
    
    if is_dark:
        dark_css = """
        /* Estilos do Tema Escuro Integral (Zero áreas brancas e tipografia branca) */
        html, body, .stApp {
            background-color: #0B0F19 !important;
            background: #0B0F19 !important;
            color: #F8FAFC !important;
        }

        /* Barra Lateral (Sidebar) no Tema Escuro */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div,
        div[data-testid="stSidebar"],
        div[data-testid="stSidebarContent"],
        div[data-testid="stSidebarUserContent"],
        [data-testid="stSidebar"] {
            background-color: #0F172A !important;
            background: #0F172A !important;
            color: #F8FAFC !important;
            border-right: 1px solid #1E293B !important;
        }
        [data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }
        [data-testid="stSidebar"] div[style*="background:#FFFFFF"],
        [data-testid="stSidebar"] div[style*="background: #FFFFFF"],
        [data-testid="stSidebar"] div[style*="background: rgb(255, 255, 255)"] {
            background-color: #1E293B !important;
            background: #1E293B !important;
            border-color: #334155 !important;
            color: #F8FAFC !important;
        }

        /* Botões secundários no Dark Mode: cinza um pouco mais claro que a tela principal (#1E293B) */
        button[kind="secondary"],
        button[data-testid="baseButton-secondary"],
        .stButton > button,
        [data-testid="stSidebar"] button,
        div[data-testid="stForm"] button[kind="secondary"],
        div[data-testid="stForm"] .stButton > button {
            background-color: #1E293B !important;
            background: #1E293B !important;
            color: #F8FAFC !important;
            border: 1px solid #334155 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
        }
        button[kind="secondary"]:hover,
        .stButton > button:hover,
        [data-testid="stSidebar"] button:hover {
            background-color: #2D3748 !important;
            background: #2D3748 !important;
            color: #FFFFFF !important;
            border-color: #38BDF8 !important;
        }
        button[kind="secondary"]:active,
        .stButton > button:active {
            background-color: #334155 !important;
            color: #FFFFFF !important;
        }

        /* Botões primários com contraste azul no escuro */
        button[kind="primary"],
        button[data-testid="baseButton-primary"],
        div[data-testid="stForm"] button[kind="primary"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        button[kind="primary"]:hover,
        button[data-testid="baseButton-primary"]:hover {
            background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
            color: #FFFFFF !important;
        }

        /* Formulários (stForm) com fundo escuro elegante (#0F172A) */
        div[data-testid="stForm"],
        div[data-testid="stForm"] > div {
            background-color: #0F172A !important;
            background: #0F172A !important;
            border: 1px solid #1E293B !important;
            border-radius: 16px !important;
            color: #F8FAFC !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        }

        /* Cards, Expanders e Contêineres de borda */
        div[style*="background:#FFFFFF"],
        div[style*="background: #FFFFFF"],
        div[style*="background: rgb(255, 255, 255)"],
        div[style*="background-color: #FFFFFF"],
        div[data-testid="stVerticalBlockBorderWrapper"] > div,
        div[data-testid="stExpander"],
        div[data-testid="stExpander"] details,
        div[data-testid="stExpander"] summary {
            background-color: #0F172A !important;
            background: #0F172A !important;
            border-color: #1E293B !important;
            color: #F8FAFC !important;
        }

        div[style*="background:#F8FAFC"],
        div[style*="background: #F8FAFC"] {
            background-color: #1E293B !important;
            background: #1E293B !important;
            border-color: #334155 !important;
            color: #F8FAFC !important;
        }

        /* Inputs, textareas, number inputs e selects: cinza escuro elegante com texto branco */
        .stTextInput input, .stNumberInput input, .stTextArea textarea,
        .stDateInput input, .stTimeInput input,
        div[data-baseweb="input"], div[data-baseweb="base-input"],
        div[data-baseweb="select"] > div,
        div[data-baseweb="select"],
        div[data-baseweb="popover"], div[data-baseweb="calendar"],
        div[data-testid="stFileUploader"] section {
            background-color: #1E293B !important;
            background: #1E293B !important;
            border-color: #334155 !important;
            color: #F8FAFC !important;
        }

        .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus,
        .stDateInput input:focus, .stTimeInput input:focus {
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
            color: #FFFFFF !important;
        }

        /* Dropdowns e Menus no Dark Mode */
        div[data-baseweb="menu"], ul[data-baseweb="menu"],
        li[data-baseweb="menu-item"] {
            background-color: #1E293B !important;
            background: #1E293B !important;
            color: #F8FAFC !important;
        }
        li[data-baseweb="menu-item"]:hover {
            background-color: #334155 !important;
            color: #38BDF8 !important;
        }

        /* Toda a tipografia deve ser branca no Dark Mode */
        h1, h2, h3, h4, h5, h6,
        p, span, label,
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] div,
        [data-testid="stMarkdownContainer"] span,
        .hero-title,
        div[style*="color:#0F172A"], div[style*="color: #0F172A"],
        span[style*="color:#0F172A"], span[style*="color: #0F172A"] {
            color: #F8FAFC !important;
        }

        /* Cores atenuadas / secundárias legíveis (#94A3B8) */
        .hero-subtitle,
        div[style*="color:#64748B"], div[style*="color: #64748B"],
        span[style*="color:#64748B"], span[style*="color: #64748B"],
        div[style*="color:#475569"], div[style*="color: #475569"],
        div[style*="color:#334155"], div[style*="color: #334155"] {
            color: #94A3B8 !important;
        }

        /* Abas Streamlit no escuro */
        .stTabs [data-baseweb="tab-list"],
        div[data-testid="stTabs"] [data-baseweb="tab-list"],
        div[data-baseweb="tab-list"] {
            border-bottom: none !important;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #0F172A !important;
            background: #0F172A !important;
            border: 1.5px solid #1E293B !important;
            color: #94A3B8 !important;
            border-radius: 14px !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            border-color: #38BDF8 !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #1E293B !important;
            background: #1E293B !important;
            color: #38BDF8 !important;
            border: 1.5px solid #38BDF8 !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2) !important;
        }

        /* Métricas */
        div[data-testid="stMetric"], div[data-testid="metric-container"] {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
        }
        div[data-testid="stMetricLabel"] p, div[data-testid="stMetricValue"] div {
            color: #F8FAFC !important;
        }
        /* SaaS Metric Card styling */
        .saas-metric-card {
            background: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 8px;
        }
        .saas-metric-icon {
            width: 44px;
            height: 44px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            background: #1E293B;
            color: #38BDF8;
        }
        .saas-metric-val {
            font-size: 1.35rem;
            font-weight: 700;
            color: #F8FAFC;
            line-height: 1.2;
        }
        .saas-metric-title {
            font-size: 0.8rem;
            color: #94A3B8;
            font-weight: 500;
        }
        """
        return f"<style>{clean_css}\n{dark_css}</style>"
    else:
        light_css = """
        /* Estilos do Tema Claro - Modern Dashboard SaaS */
        html, body, .stApp {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
        }
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        /* SaaS Card styling for Light Mode */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            border-radius: 14px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
            background: #FFFFFF !important;
        }

        /* Abas Streamlit no tema claro */
        .stTabs [data-baseweb="tab-list"],
        div[data-testid="stTabs"] [data-baseweb="tab-list"],
        div[data-baseweb="tab-list"] {
            border-bottom: none !important;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: 1.5px solid #E2E8F0 !important;
            color: #334155 !important;
            border-radius: 14px !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
            border-color: #CBD5E1 !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #EEF2FF !important;
            background: #EEF2FF !important;
            color: #4F46E5 !important;
            border: 1.5px solid #6366F1 !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
        }
        .saas-metric-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }
        .saas-metric-icon {
            width: 44px;
            height: 44px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            background: #F1F5F9;
            color: #2563EB;
        }
        .saas-metric-val {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
        }
        .saas-metric-title {
            font-size: 0.8rem;
            color: #64748B;
            font-weight: 500;
        }
        """
        return f"<style>{clean_css}\n{light_css}</style>"






