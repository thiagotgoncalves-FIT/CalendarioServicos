"""
AgendAí — Plataforma de Gestão e Agendamento para Prestadores Independentes
Frontend principal desenvolvido em Streamlit conectado ao backend Xano.
"""

import streamlit as st
import importlib
import base64
from datetime import date, datetime, time
from services import (
    auth_service,
    api_client,
    catalog_service,
    availability_service,
    appointment_service,
    ui_utils,
    recommendation_service,
    review_service
)

# Força o recarregamento dinâmico dos submódulos no runtime do Streamlit
importlib.reload(auth_service)
importlib.reload(review_service)
importlib.reload(ui_utils)

st.set_page_config(
    page_title="AgendAí — Gestão e Agendamento",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "view_mode" not in st.session_state:
    st.session_state["view_mode"] = "dashboard"

# Determina e aplica o tema ativo (Claro ou Escuro) e limpa artefatos técnicos da interface
current_active_theme = "claro"
if st.session_state.get("authenticated") and isinstance(st.session_state.get("user"), dict):
    current_active_theme = st.session_state["user"].get("theme", "claro")

# Base de fontes universais
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Aplica regras específicas apenas para o Tema Claro (evitando sobrepor o Tema Escuro)
if current_active_theme == "claro":
    st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }

    /* Container e Cabeçalho */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #475569;
        font-size: 1.05rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }

    /* Cards e Formulários com Fundo Branco */
    div[data-testid="stForm"] {
        background: #FFFFFF !important;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
    }

    /* Todos os Widgets com Fundo Branco Puro */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea,
    .stDateInput input, .stTimeInput input,
    div[data-baseweb="input"], div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"],
    div[data-testid="stExpander"], div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] summary,
    div[data-testid="stMetric"], div[data-testid="metric-container"],
    div[data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stAlert"],
    div[data-baseweb="popover"], div[data-baseweb="calendar"],
    div[data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
        color: #0F172A !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }

    .stTextInput input, .stNumberInput input, .stTextArea textarea,
    .stDateInput input, .stTimeInput input {
        border-radius: 10px !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease !important;
        background-color: #FFFFFF !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus,
    .stDateInput input:focus, .stTimeInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        background-color: #FFFFFF !important;
    }

    /* Alertas e Notificações com Fundo Branco */
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        color: #0F172A !important;
    }

    /* Expanders Brancos */
    div[data-testid="stExpander"] {
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
        margin-bottom: 0.75rem !important;
        background-color: #FFFFFF !important;
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #0F172A !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
    }

    /* Botões Primários Azuis */
    div[data-testid="stForm"] button[kind="primary"], button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.25rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    }
    div[data-testid="stForm"] button[kind="primary"]:hover, button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35) !important;
    }

    /* Botões Secundários Brancos */
    button[kind="secondary"], .stButton > button {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    button[kind="secondary"]:hover, .stButton > button:hover {
        background-color: #EFF6FF !important;
        border-color: #2563EB !important;
        color: #1D4ED8 !important;
    }

    /* Dropdowns, Calendários e Menus Brancos */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"],
    div[data-baseweb="calendar"], div[data-baseweb="calendar"] * {
        background-color: #FFFFFF !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
    }
    li[data-baseweb="menu-item"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[data-baseweb="menu-item"]:hover {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
    }

    /* Tabs Customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        color: #64748B !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        border: 1px solid #E2E8F0 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
        border: 1px solid #2563EB !important;
    }

    /* Cards e Containers com fundo branco e bordas suaves */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* Ocultar permanentemente botões de colapso da sidebar */
    button[data-testid="stSidebarCollapseButton"],
    div[data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

    /* Limpeza de elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Aplica o tema ativo e limpa artefatos técnicos da interface
st.markdown(ui_utils.apply_theme_and_clean_ui(current_active_theme), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Gerenciamento de Estado da Sessão (Session State)
# -----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None
if "show_recovery" not in st.session_state:
    st.session_state["show_recovery"] = False
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"


def do_logout():
    """Limpa os dados de autenticação e encerra a sessão com redirecionamento limpo."""
    st.session_state["authenticated"] = False
    st.session_state["auth_token"] = None
    st.session_state["user"] = None
    st.session_state["show_recovery"] = False
    st.session_state["auth_page"] = "login"
    st.rerun()


# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    if st.session_state["authenticated"]:
        user = st.session_state["user"]
        role = user.get("role", "cliente")
        role_label = "Prestador Autônomo" if role == "prestador" else "Cliente"
        badge_style = (
            "background:#EFF6FF; color:#1D4ED8; border:1px solid #BFDBFE;"
            if role == "prestador"
            else "background:#ECFDF5; color:#047857; border:1px solid #A7F3D0;"
        )
        avatar_html = ui_utils.user_avatar_html(user, size=42)

        # Cabeçalho Superior Unificado: Marca + Perfil do Usuário Logado
        st.markdown(
            f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:0.9rem 1rem; margin-bottom:0.75rem; box-shadow:0 1px 3px rgba(0,0,0,0.05);">'
            f'<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; padding-bottom:6px; border-bottom:1px solid #F1F5F9;">'
            f'<div style="display:flex; align-items:center; gap:8px;">'
            f'<div style="width:26px; height:26px; border-radius:6px; background:linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.8rem; color:#FFFFFF;">A</div>'
            f'<span style="font-size:0.95rem; font-weight:800; color:#0F172A; letter-spacing:-0.01em;">AgendAí</span>'
            f'</div>'
            f'<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.7rem; font-weight:700; {badge_style}">{role_label}</span>'
            f'</div>'
            f'<div style="display:flex; align-items:center; gap:10px;">'
            f'{avatar_html}'
            f'<div style="overflow:hidden; line-height:1.2;">'
            f'<div style="font-size:0.95rem; font-weight:700; color:#0F172A; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user.get("name", "Usuário")}</div>'
            f'<div style="font-size:0.75rem; color:#64748B; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user.get("email", "")}</div>'
            f'</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        col_side_cfg, col_side_out = st.columns([1, 1])
        with col_side_cfg:
            is_settings = (st.session_state.get("view_mode") == "settings")
            if is_settings:
                if st.button("🏠 Início", key="btn_sidebar_home", help="Voltar ao Painel Principal com seus agendamentos", use_container_width=True, type="primary"):
                    st.session_state["view_mode"] = "dashboard"
                    st.rerun()
            else:
                if st.button("⚙️ Ajustes", key="btn_sidebar_settings", help="Abrir Configurações da Conta", use_container_width=True, type="secondary"):
                    st.session_state["view_mode"] = "settings"
                    st.rerun()
        with col_side_out:
            if st.button("Sair", use_container_width=True, type="secondary"):
                do_logout()
    else:
        st.markdown(
            '<div style="display:flex; align-items:center; gap:12px; margin-bottom:1.2rem;">'
            '<div style="width:38px; height:38px; border-radius:10px; background:linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.1rem; color:#FFFFFF; box-shadow:0 4px 10px rgba(37,99,235,0.25);">A</div>'
            '<div><div style="font-size:1.35rem; font-weight:800; color:#0F172A; line-height:1.1;">AgendAí</div>'
            '<div style="font-size:0.75rem; color:#64748B;">Gestão e Agendamento</div></div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.info("Faça login ou crie sua conta para acessar o AgendAí.")


@st.dialog("Detalhes do Serviço")
def show_service_details_dialog(servico: dict, token: Optional[str] = None, user: Optional[dict] = None):
    """Janela modal independente contendo informações detalhadas e avaliações exclusivas do serviço."""
    s_id = servico.get("id")
    p_id = servico.get("prestador_id", 15)
    dur_min = servico.get("duracao_minutos", 30)
    preco = servico.get("preco", 0)

    st.markdown(f"### {servico.get('titulo')}")

    if servico.get("descricao"):
        st.markdown(f"<p style='color:#475569; font-size:0.95rem; line-height:1.5;'>{servico.get('descricao')}</p>", unsafe_allow_html=True)

    col_info1, col_info2 = st.columns(2)
    col_info1.markdown(f"**Valor:** {ui_utils.format_currency_brl(preco)}")
    col_info2.markdown(f"**Duração:** {dur_min} min")

    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
    st.markdown("#### Avaliações deste Serviço")

    try:
        m_serv = review_service.get_metrics(servico_id=s_id, token=token)
    except TypeError:
        importlib.reload(review_service)
        m_serv = review_service.get_metrics(servico_id=s_id, token=token)
    st.markdown(ui_utils.service_reviews_summary_html(m_serv["nota_media"], m_serv["total_avaliacoes"]), unsafe_allow_html=True)

    _, revs = review_service.get_reviews(servico_id=s_id, token=token)
    if revs:
        key_lim = f"dlg_rev_lim_{s_id}"
        if key_lim not in st.session_state:
            st.session_state[key_lim] = 5
        limit = st.session_state[key_lim]

        for r in revs[:limit]:
            dt_raw = r.get("criado_em", "").split()[0] if r.get("criado_em") else ""
            dt_fmt = ui_utils.format_date_short_pt_br(dt_raw)
            st.markdown(
                ui_utils.review_card_html(
                    nome=r.get("cliente_nome_exibicao", "Cliente"),
                    rating=int(r.get("nota", 5)),
                    data_str=dt_fmt or "Recente",
                    comentario=r.get("comentario", "")
                ),
                unsafe_allow_html=True
            )

        if len(revs) > limit:
            if st.button("Carregar Mais Avaliações", key=f"btn_more_dlg_{s_id}", use_container_width=True, type="secondary"):
                st.session_state[key_lim] += 5
                st.rerun()
    else:
        st.markdown(
            ui_utils.empty_state_html(
                "",
                "Este serviço ainda não possui avaliações",
                "Seja o primeiro a agendar e avaliar após a conclusão do atendimento!"
            ),
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

    with st.expander("📅 Agendar este Serviço", expanded=False):
        dt_dlg = st.date_input("Data do Atendimento", min_value=date.today(), value=date.today(), key=f"dlg_dt_{s_id}")
        dt_dlg_str = dt_dlg.strftime("%Y-%m-%d")
        slots_dlg = appointment_service.calculate_available_slots(p_id, dt_dlg_str, dur_min, token=token)
        if slots_dlg:
            slot_sel = st.selectbox("Horários livres disponíveis:", options=slots_dlg, key=f"dlg_slot_{s_id}")
            if st.button("Confirmar Agendamento", key=f"dlg_btn_conf_{s_id}", type="primary", use_container_width=True):
                cli_id = user.get("id", 0) if user else 0
                cli_nome = user.get("name", "Cliente") if user else "Cliente"
                cli_tel = user.get("phone", "") if user else ""
                with st.spinner("Confirmando agendamento..."):
                    suc, resp = appointment_service.create_appointment(
                        cliente_id=cli_id,
                        prestador_id=p_id,
                        servico_id=s_id,
                        data_str=dt_dlg_str,
                        hora_inicio=slot_sel,
                        token=token,
                        cliente_nome=cli_nome,
                        cliente_telefone=cli_tel
                    )
                if suc:
                    st.toast("Agendamento confirmado com sucesso!")
                    st.success(f"Agendado para {ui_utils.format_date_short_pt_br(dt_dlg)} às {slot_sel}!")
                    st.rerun()
                else:
                    st.error(f"{resp.get('message', 'Erro ao agendar.')}")
        else:
            st.warning("Nenhum horário livre disponível para esta data.")

    if st.button("Fechar", key=f"dlg_close_{s_id}", use_container_width=True, type="secondary"):
        st.rerun()


@st.dialog("Avalie seu Atendimento")
def show_review_appointment_dialog(app: dict, user: dict, token: Optional[str] = None):
    """Janela modal para o cliente avaliar um atendimento concluído."""
    app_id = app.get("id")
    serv_titulo = app.get("servico_titulo", "Serviço Contratado")
    data_br = ui_utils.format_date_short_pt_br(app.get("data"))

    st.markdown(f"### Como foi seu atendimento?")
    st.markdown(f"Conte-nos o que achou de **{serv_titulo}** realizado em **{data_br}**.")

    with st.form(f"form_dialog_review_{app_id}"):
        nota = st.slider("Sua nota (1 a 5 estrelas) *", min_value=1, max_value=5, value=5, step=1, key=f"dlg_nota_{app_id}")
        comentario = st.text_area(
            "Comentário (opcional, máximo 500 caracteres):",
            placeholder="Compartilhe sua experiência com este serviço...",
            max_chars=500,
            key=f"dlg_coment_{app_id}"
        )
        col_sub1, col_sub2 = st.columns(2)
        with col_sub1:
            btn_enviar = st.form_submit_button("Enviar Avaliação", type="primary", use_container_width=True)
        with col_sub2:
            btn_depois = st.form_submit_button("Avaliar Mais Tarde", type="secondary", use_container_width=True)

        if btn_enviar:
            with st.spinner("Gravando sua avaliação..."):
                suc_rev, resp_rev = review_service.submit_review(
                    agendamento_id=app_id,
                    cliente_id=user.get("id", 0),
                    prestador_id=app.get("prestador_id", 15),
                    nota=nota,
                    comentario=comentario,
                    cliente_nome=user.get("name", "Cliente"),
                    servico_id=app.get("servico_id"),
                    servico_titulo=app.get("servico_titulo"),
                    token=token
                )
            if suc_rev:
                st.toast("Obrigado! Sua avaliação foi enviada com sucesso.")
                st.session_state[f"dismissed_review_dialog_{app_id}"] = True
                st.session_state["review_dialog_shown"] = True
                st.rerun()
            else:
                st.error(f"{resp_rev.get('message', 'Erro ao enviar avaliação.')}")

        if btn_depois:
            st.session_state[f"dismissed_review_dialog_{app_id}"] = True
            st.rerun()


def render_public_reviews_tab(token=None):
    """Renderiza a aba pública com métricas e listagem de avaliações dos clientes com filtro por serviço."""
    st.subheader("Avaliações e Satisfação dos Clientes")
    st.markdown("Confira os depoimentos e notas de quem já utilizou os serviços na plataforma.")

    # Filtro opcional por serviço
    suc_serv, lista_servicos = catalog_service.get_public_services(token=token)
    opcoes_filtro = [{"id": None, "titulo": "Todos os Serviços"}]
    if suc_serv and lista_servicos:
        for s in lista_servicos:
            opcoes_filtro.append({"id": s.get("id"), "titulo": s.get("titulo")})

    col_filtro, _ = st.columns([2, 1])
    with col_filtro:
        filtro_selecionado = st.selectbox(
            "Filtrar avaliações por serviço:",
            options=opcoes_filtro,
            format_func=lambda opt: opt["titulo"],
            key="filtro_geral_avaliacoes_servico"
        )
    servico_id_filtro = filtro_selecionado.get("id") if filtro_selecionado else None

    try:
        metrics = review_service.get_metrics(servico_id=servico_id_filtro, token=token)
    except TypeError:
        importlib.reload(review_service)
        metrics = review_service.get_metrics(servico_id=servico_id_filtro, token=token)
    nota_media = metrics.get("nota_media", 0.0)
    total_avaliacoes = metrics.get("total_avaliacoes", 0)

    # Cards de resumo
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        stars_repr = ui_utils.render_stars_html(nota_media)
        sub_desc = filtro_selecionado["titulo"] if filtro_selecionado and filtro_selecionado.get("id") else "Baseado na opinião de clientes reais"
        st.markdown(
            f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.25rem 1.5rem; box-shadow:0 1px 4px rgba(0,0,0,0.05);">'
            f'<span style="font-size:0.85rem; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">Nota Média</span>'
            f'<div style="margin-top:0.35rem; display:flex; align-items:center; gap:8px;">'
            f'{stars_repr}'
            f'</div>'
            f'<div style="font-size:0.8rem; color:#64748B; margin-top:0.35rem;">{sub_desc}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col_m2:
        st.markdown(
            ui_utils.metric_card_html(
                "Total de Avaliações",
                str(total_avaliacoes),
                "Feedbacks autênticos de clientes verificados"
            ),
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("### Depoimentos Recentes")

    _, reviews = review_service.get_reviews(servico_id=servico_id_filtro, token=token)

    if reviews:
        if "reviews_limit" not in st.session_state:
            st.session_state["reviews_limit"] = 5

        limit = st.session_state["reviews_limit"]
        exibidos = reviews[:limit]

        for rev in exibidos:
            dt_raw = rev.get("criado_em", "").split()[0] if rev.get("criado_em") else ""
            dt_fmt = ui_utils.format_date_short_pt_br(dt_raw)
            st.markdown(
                ui_utils.review_card_html(
                    nome=rev.get("cliente_nome_exibicao", "Cliente"),
                    rating=int(rev.get("nota", 5)),
                    data_str=dt_fmt or "Recente",
                    comentario=rev.get("comentario", ""),
                    servico_titulo=rev.get("servico_titulo")
                ),
                unsafe_allow_html=True
            )

        if len(reviews) > limit:
            if st.button("Carregar Mais Avaliações", use_container_width=True, type="secondary"):
                st.session_state["reviews_limit"] += 5
                st.rerun()
    else:
        st.markdown(
            ui_utils.empty_state_html(
                "",
                "Nenhuma avaliação encontrada",
                "Ainda não há avaliações registradas para a opção selecionada."
            ),
            unsafe_allow_html=True
        )


def render_account_settings_view(user: dict):
    """
    Renderiza a tela dedicada de Configurações da Conta.
    Permite gerenciar foto de perfil, dados cadastrais, tema (aparência) e alteração de senha.
    """
    col_hdr1, col_hdr2 = st.columns([5, 1])
    with col_hdr1:
        st.markdown(
            f'<div style="margin-bottom:1rem;">'
            f'<div style="font-size:2rem; font-weight:800; color:#0F172A; margin-bottom:0.25rem;">⚙️ Configurações da Conta</div>'
            f'<div style="font-size:0.95rem; color:#64748B;">Gerencie seu perfil, preferências visuais e segurança de acesso.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col_hdr2:
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        if st.button("⬅️ Voltar", key="btn_back_to_dashboard", use_container_width=True, type="primary"):
            st.session_state["view_mode"] = "dashboard"
            st.rerun()

    tab_cfg_perfil, tab_cfg_tema, tab_cfg_seguranca = st.tabs([
        "👤 Perfil e Foto", "🎨 Aparência (Tema)", "🔒 Segurança e Senha"
    ])

    # -------------------------------------------------------------------------
    # Aba 1: Foto e Dados Pessoais
    # -------------------------------------------------------------------------
    with tab_cfg_perfil:
        st.markdown("#### Foto de Perfil")
        col_avatar_view, col_avatar_upload = st.columns([1, 3])
        with col_avatar_view:
            st.markdown(ui_utils.user_avatar_html(user, size=110), unsafe_allow_html=True)
            if user.get("photo_url"):
                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                if st.button("Remover Foto", key="btn_remove_avatar", use_container_width=True, type="secondary"):
                    suc_rem, resp_rem = auth_service.remove_user_avatar(user.get("id", 0))
                    if suc_rem:
                        st.session_state["user"]["photo_url"] = None
                        st.session_state["user"]["photo_rel_url"] = None
                        st.toast("Foto de perfil removida com sucesso!")
                        st.rerun()
                    else:
                        st.error(resp_rem.get("message", "Erro ao remover foto."))

        with col_avatar_upload:
            uploaded_file = st.file_uploader(
                "Enviar nova foto de perfil",
                type=["jpg", "jpeg", "png", "webp"],
                help="Selecione uma imagem JPG, PNG ou WebP de até 2 MB."
            )
            if uploaded_file is not None:
                if uploaded_file.size > 2 * 1024 * 1024:
                    st.error("A imagem selecionada excede o limite máximo permitido de 2 MB.")
                else:
                    b64_preview = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                    ext_prev = uploaded_file.name.split(".")[-1].lower()
                    mime_prev = "jpeg" if ext_prev in ("jpg", "jpeg") else ext_prev
                    st.markdown(
                        f'<div style="display:flex; align-items:center; gap:12px; margin-top:0.5rem; margin-bottom:0.5rem;">'
                        f'<div style="width:56px; height:56px; border-radius:50%; overflow:hidden; border:2px solid #2563EB;">'
                        f'<img src="data:image/{mime_prev};base64,{b64_preview}" style="width:100%; height:100%; object-fit:cover;" />'
                        f'</div>'
                        f'<span style="font-size:0.85rem; color:#64748B;">Pré-visualização da imagem</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    if st.button("Salvar Nova Foto", key="btn_save_avatar", type="primary"):
                        suc_save, resp_save = auth_service.save_user_avatar(
                            user.get("id", 0),
                            uploaded_file.getvalue(),
                            uploaded_file.name
                        )
                        if suc_save:
                            st.session_state["user"]["photo_url"] = resp_save.get("photo_url")
                            st.session_state["user"]["photo_rel_url"] = resp_save.get("photo_rel_url")
                            st.toast("Foto de perfil atualizada com sucesso!")
                            st.rerun()
                        else:
                            st.error(resp_save.get("message", "Erro ao salvar imagem."))

        st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #E2E8F0;'/>", unsafe_allow_html=True)
        st.markdown("#### Dados Cadastrais")

        with st.form("form_edit_user_profile"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                edit_name = st.text_input("Nome Completo", value=user.get("name", ""), max_chars=100)
            with col_f2:
                tel_atual = auth_service.format_phone_br(user.get("phone", ""))
                edit_phone = st.text_input("Telefone com DDD", value=tel_atual, placeholder="(11) 99999-9999", help="Informe DDD + número (10 ou 11 dígitos)")

            st.text_input(
                "E-mail",
                value=user.get("email", ""),
                disabled=True,
                help="O e-mail é a credencial principal da sua conta e não pode ser alterado."
            )

            submit_profile = st.form_submit_button("Salvar Alterações Cadastrais", type="primary")

        if submit_profile:
            suc_upd, resp_upd = auth_service.update_user_profile(
                user.get("id", 0),
                edit_name,
                edit_phone,
                token=st.session_state.get("auth_token"),
                email=user.get("email")
            )
            if suc_upd:
                updated_user = resp_upd.get("user", {})
                st.session_state["user"]["name"] = updated_user.get("name", edit_name.strip())
                st.session_state["user"]["phone"] = updated_user.get("phone", edit_phone)
                if updated_user.get("phone_formatted"):
                    st.session_state["user"]["phone_formatted"] = updated_user.get("phone_formatted")
                st.toast("Dados pessoais atualizados com sucesso!")
                st.rerun()
            else:
                st.error(resp_upd.get("message", "Erro ao atualizar dados."))

    # -------------------------------------------------------------------------
    # Aba 2: Aparência (Tema)
    # -------------------------------------------------------------------------
    with tab_cfg_tema:
        st.markdown("#### Escolha o Tema da Interface")
        st.caption("Personalize as cores do AgendAí para a sua conta. A escolha será lembrada em todos os seus dispositivos.")

        current_theme = (user.get("theme") or "claro").lower()
        theme_options = ["Claro", "Escuro"]
        theme_idx = 0 if current_theme == "claro" else 1

        chosen_theme_label = st.radio(
            "Tema Ativo",
            options=theme_options,
            index=theme_idx,
            horizontal=True,
            help="O tema Claro é otimizado para ambientes iluminados e o Escuro para menor fadiga visual."
        )

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            with st.container(border=True):
                st.markdown("☀️ **Tema Claro**")
                st.caption("Fundo claro e neutro com alto contraste e acabamento profissional em azul.")
        with col_t2:
            with st.container(border=True):
                st.markdown("🌙 **Tema Escuro**")
                st.caption("Fundo Obsidian/Slate moderno com descanso visual para uso prolongado.")

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
        target_theme = chosen_theme_label.lower()
        if target_theme != current_theme:
            if st.button("Aplicar Preferência de Tema", type="primary", key="btn_apply_theme"):
                suc_theme, resp_theme = auth_service.update_user_theme(
                    user.get("id", 0),
                    target_theme,
                    token=st.session_state.get("auth_token")
                )
                if suc_theme:
                    st.session_state["user"]["theme"] = target_theme
                    st.toast(f"Tema alterado para {chosen_theme_label} com sucesso!")
                    st.rerun()
                else:
                    st.error(resp_theme.get("message", "Erro ao atualizar tema."))
        else:
            st.info(f"O tema **{chosen_theme_label}** já está ativo no seu perfil.")

    # -------------------------------------------------------------------------
    # Aba 3: Segurança e Senha
    # -------------------------------------------------------------------------
    with tab_cfg_seguranca:
        st.markdown("#### Alteração de Senha")
        st.caption("Para sua segurança, informe sua senha atual antes de cadastrar uma nova senha.")

        with st.form("form_change_password"):
            cur_pass = st.text_input("Senha Atual", type="password", placeholder="Digite sua senha atual")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                new_pass = st.text_input("Nova Senha", type="password", placeholder="Mínimo 8 caracteres (letras e números)")
            with col_p2:
                conf_pass = st.text_input("Confirmação da Nova Senha", type="password", placeholder="Repita a nova senha")

            submit_pass = st.form_submit_button("Atualizar Senha", type="primary")

        if submit_pass:
            suc_pass, resp_pass = auth_service.change_password(
                user.get("id", 0),
                cur_pass,
                new_pass,
                conf_pass,
                token=st.session_state.get("auth_token"),
                email=user.get("email")
            )
            if suc_pass:
                st.success("Senha alterada com sucesso! Utilize a nova senha no seu próximo login.")
            else:
                st.error(resp_pass.get("message", "Não foi possível alterar a senha."))


# -----------------------------------------------------------------------------
# Interface Principal: Não Autenticado (Login / Cadastro)
# -----------------------------------------------------------------------------
if not st.session_state["authenticated"]:
    # -------------------------------------------------------------------------
    # TELA EXCLUSIVA 1: LOGIN
    # -------------------------------------------------------------------------
    if st.session_state.get("auth_page", "login") == "login":
        st.markdown('<div class="hero-title">Bem-vindo ao AgendAí</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-subtitle">Acesse sua conta para agendar atendimentos ou gerenciar sua agenda profissional de forma simples e rápida.</div>',
            unsafe_allow_html=True
        )

        with st.form("form_login"):
            email_login = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
            pass_login = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submit_login = st.form_submit_button("Entrar no AgendAí", use_container_width=True, type="primary")

            if submit_login:
                with st.spinner("Autenticando..."):
                    success, response = auth_service.login(email_login, pass_login)
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["auth_token"] = response.get("authToken")
                    st.session_state["user"] = response.get("user")
                    st.toast("Login realizado com sucesso.")
                    st.rerun()
                else:
                    st.error(f"{response.get('message', 'Erro ao efetuar login.')}")

        # Ação única para navegação direta para Cadastro
        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
        if st.button("Não tem uma conta? Criar conta", use_container_width=True, type="secondary"):
            st.session_state["auth_page"] = "signup"
            st.rerun()

        if not st.session_state.get("show_recovery"):
            if st.button("Esqueceu sua senha?", use_container_width=True):
                st.session_state["show_recovery"] = True
                st.session_state["recovery_step"] = "email"
                st.rerun()
        else:
            st.markdown("---")
            rec_step = st.session_state.get("recovery_step", "email")

            # -------------------------------------------------------------
            # Etapa 1: Validação do E-mail Cadastrado
            # -------------------------------------------------------------
            if rec_step == "email":
                st.markdown("#### Recuperação de Senha")
                st.info("Informe o e-mail cadastrado na sua conta para enviarmos um código de validação.")

                with st.form("form_recovery_email"):
                    email_input = st.text_input("Seu e-mail cadastrado", placeholder="seu.email@exemplo.com")
                    submit_send_code = st.form_submit_button("Gerar Código de Verificação", use_container_width=True, type="primary")

                if submit_send_code:
                    clean_em = email_input.strip().lower()
                    if not clean_em or "@" not in clean_em:
                        st.error("Por favor, digite um endereço de e-mail válido.")
                    else:
                        code_generated = auth_service.generate_recovery_code()
                        st.session_state["recovery_email"] = clean_em
                        st.session_state["recovery_code"] = code_generated
                        st.session_state["recovery_step"] = "code"
                        st.toast("Código de validação gerado com sucesso!")
                        st.rerun()

            # -------------------------------------------------------------
            # Etapa 2: Validação do Código de 6 Dígitos no App
            # -------------------------------------------------------------
            elif rec_step == "code":
                rec_em = st.session_state.get("recovery_email", "")
                rec_code = st.session_state.get("recovery_code", "")

                st.markdown("#### Confirmação do Código de Segurança")
                st.caption(f"Conta identificada: **{rec_em}**")

                # Caixa com o código gerado no app
                st.markdown(
                    f'<div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:1.2rem; text-align:center; margin:1rem 0;">'
                    f'<div style="font-size:0.85rem; color:#1E40AF; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.4rem;">Seu Código de Confirmação</div>'
                    f'<div style="font-size:2.2rem; font-weight:800; color:#1D4ED8; letter-spacing:0.2em; font-family:monospace;">{rec_code}</div>'
                    f'<div style="font-size:0.8rem; color:#3B82F6; margin-top:0.4rem;">Insira o código acima no campo abaixo para autorizar a redefinição de sua senha.</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                with st.form("form_recovery_code"):
                    code_digitado = st.text_input("Digite o código de 6 dígitos exibido acima", max_chars=6, placeholder="Ex: 123456")
                    submit_verify_code = st.form_submit_button("Validar Código", use_container_width=True, type="primary")

                if submit_verify_code:
                    if code_digitado.strip() == rec_code:
                        st.session_state["recovery_step"] = "new_password"
                        st.toast("Código validado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Código incorreto. Por favor, digite o código exibido acima e tente novamente.")

            # -------------------------------------------------------------
            # Etapa 3: Definição da Nova Senha
            # -------------------------------------------------------------
            elif rec_step == "new_password":
                rec_em = st.session_state.get("recovery_email", "")
                st.markdown("#### Criar Nova Senha")
                st.caption(f"Defina uma nova senha para a conta: **{rec_em}**")

                with st.form("form_recovery_new_pass"):
                    new_p = st.text_input("Nova Senha", type="password", placeholder="Mínimo 8 caracteres (letras e números)")
                    conf_p = st.text_input("Confirme a Nova Senha", type="password", placeholder="Repita a nova senha")
                    submit_reset = st.form_submit_button("Redefinir e Salvar Senha", use_container_width=True, type="primary")

                if submit_reset:
                    suc_res, resp_res = auth_service.reset_password_with_recovery(rec_em, new_p, conf_p)
                    if suc_res:
                        st.toast("Senha redefinida com sucesso!")
                        st.success(resp_res.get("message", "Senha alterada com sucesso!"))
                        st.session_state["show_recovery"] = False
                        st.session_state["recovery_step"] = "email"
                        st.session_state["recovery_code"] = None
                        st.session_state["recovery_email"] = None
                    else:
                        st.error(resp_res.get("message", "Erro ao redefinir a senha."))

            # Botão para cancelar ou voltar ao login
            col_b_voltar, col_b_reiniciar = st.columns(2)
            with col_b_voltar:
                if st.button("Voltar para o Login", use_container_width=True, type="secondary"):
                    st.session_state["show_recovery"] = False
                    st.session_state["recovery_step"] = "email"
                    st.rerun()
            with col_b_reiniciar:
                if rec_step != "email":
                    if st.button("Recomeçar Recuperação", use_container_width=True):
                        st.session_state["recovery_step"] = "email"
                        st.rerun()

    # -------------------------------------------------------------------------
    # TELA EXCLUSIVA 2: CADASTRO
    # -------------------------------------------------------------------------
    elif st.session_state.get("auth_page") == "signup":
        st.markdown('<div class="hero-title">Crie sua conta no AgendAí</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-subtitle">Preencha seus dados para começar a agendar serviços ou disponibilizar seus atendimentos como profissional autônomo.</div>',
            unsafe_allow_html=True
        )

        with st.form("form_signup"):
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                name_signup = st.text_input("Nome Completo / Nome Fantasia", placeholder="Ex: Lucas Ferreira")
                email_signup = st.text_input("E-mail", placeholder="exemplo@email.com")
                phone_signup = st.text_input("WhatsApp / Telefone", placeholder="(11) 99999-9999")
            with col_u2:
                pass_signup = st.text_input("Senha", type="password", placeholder="Mínimo 8 caracteres (letras e números)")
                pass_confirm = st.text_input("Confirmação de Senha", type="password", placeholder="Repita a senha digitada")
                role_choice = st.radio(
                    "Qual é o seu perfil de uso?",
                    options=["cliente", "prestador"],
                    format_func=lambda r: "Cliente (agendar serviços com facilidade)" if r == "cliente" else "Prestador de Serviços (divulgar horários e gerenciar clientes)",
                    horizontal=False
                )

            submit_signup = st.form_submit_button("Cadastrar e Começar", use_container_width=True, type="primary")

            if submit_signup:
                if not pass_signup or pass_signup != pass_confirm:
                    st.error("As senhas digitadas não coincidem. Por favor, verifique.")
                else:
                    with st.spinner("Criando sua conta com segurança..."):
                        success, response = auth_service.signup(
                            name=name_signup,
                            email=email_signup,
                            password=pass_signup,
                            phone=phone_signup,
                            role=role_choice
                        )
                    if success:
                        st.session_state["authenticated"] = True
                        st.session_state["auth_token"] = response.get("authToken")
                        st.session_state["user"] = response.get("user")
                        st.session_state["auth_page"] = "login"
                        st.toast("Conta criada com sucesso.")
                        st.rerun()
                    else:
                        st.error(f"{response.get('message', 'Erro ao criar conta.')}")

        # Ação única para retornar ao Login
        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
        if st.button("Já tem uma conta? Entrar", use_container_width=True, type="secondary"):
            st.session_state["auth_page"] = "login"
            st.rerun()


# -----------------------------------------------------------------------------
# Interface Principal: Usuário Autenticado
# -----------------------------------------------------------------------------
else:
    user = st.session_state["user"]
    role = user.get("role", "cliente")
    is_settings = (st.session_state.get("view_mode") == "settings")

    # Barra de Navegação Superior (Fora da Sidebar)
    # No modo dashboard, disponibiliza atalho para Configurações
    if not is_settings:
        col_nav_info, col_nav_act = st.columns([4, 1.8])
        with col_nav_info:
            role_desc = "Painel do Prestador Autônomo" if role == "prestador" else "Painel e Atendimentos do Cliente"
            st.caption(f"📍 **AgendAí** • {role_desc}")
        with col_nav_act:
            if st.button("⚙️ Configurações", key="btn_main_go_to_settings", help="Abrir Configurações da Conta (Foto, Tema, Senha)", type="secondary", use_container_width=True):
                st.session_state["view_mode"] = "settings"
                st.rerun()
        st.markdown("<hr style='margin: 0.25rem 0 1.25rem 0; border: none; border-top: 1px solid #E2E8F0;'/>", unsafe_allow_html=True)

    # Verifica se o usuário está na tela de configurações da conta
    if is_settings:
        render_account_settings_view(user)

    # =========================================================================
    # VISÃO DO PRESTADOR DE SERVIÇOS
    # =========================================================================
    elif role == "prestador":
        # Cabeçalho do Prestador
        nome_prestador = user.get('name', 'Prestador')
        data_formatada = ui_utils.format_date_long_pt_br()

        st.markdown(
            f'<div style="margin-bottom:1.5rem;">'
            f'<div style="font-size:2rem; font-weight:800; color:#0F172A; margin-bottom:0.25rem;">Olá, {nome_prestador}!</div>'
            f'<div style="font-size:0.95rem; color:#64748B; display:flex; align-items:center; gap:8px;">'
            f'<span>Painel do Prestador</span><span>•</span><span>{data_formatada}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        tab_resumo, tab_agenda, tab_catalogo, tab_grade = st.tabs([
            "📊 Resumo", "📅 Agenda de Atendimentos", "✂️ Meus Serviços", "⏰ Grade de Atendimento"
        ])

        # ---------------------------------------------------------------------
        # Aba 1: Resumo
        # ---------------------------------------------------------------------
        with tab_resumo:
            sucesso_cat, servicos = catalog_service.get_services(user.get("id", 0), st.session_state.get("auth_token"))
            ativos = [s for s in servicos if s.get("ativo")] if sucesso_cat and servicos else []
            qtd_ativos = len(ativos)
            preco_medio = sum(float(s["preco"]) for s in ativos) / qtd_ativos if qtd_ativos > 0 else 0.0

            _, prestador_apps = appointment_service.get_appointments_by_user(user.get("id", 0), role="prestador", token=st.session_state.get("auth_token"))
            today_str = date.today().strftime("%Y-%m-%d")
            apps_hoje = [a for a in prestador_apps if a.get("data") == today_str and ui_utils.normalize_status(a.get("status")) in ("confirmado", "pendente", "concluido")] if prestador_apps else []
            receita_prevista = sum(float(a.get("valor_cobrado", 0)) for a in prestador_apps if ui_utils.normalize_status(a.get("status")) in ("confirmado", "concluido")) if prestador_apps else 0.0

            # 3 Cards de Métricas Neutros e Profissionais
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                sub_hoje = f"{len(apps_hoje)} agendamento(s) para hoje" if len(apps_hoje) > 0 else "Nenhum agendamento para hoje"
                st.markdown(ui_utils.metric_card_html("Agendamentos Hoje", str(len(apps_hoje)), sub_hoje), unsafe_allow_html=True)
            with col_m2:
                sub_ativos = "Disponíveis para clientes" if qtd_ativos > 0 else "Nenhum serviço ativo"
                st.markdown(ui_utils.metric_card_html("Serviços Ativos", str(qtd_ativos), sub_ativos), unsafe_allow_html=True)
            with col_m3:
                sub_preco = f"Receita prevista: {ui_utils.format_currency_brl(receita_prevista)}" if receita_prevista > 0 else "Base de serviços ativos"
                st.markdown(ui_utils.metric_card_html("Preço Médio", ui_utils.format_currency_brl(preco_medio), sub_preco), unsafe_allow_html=True)

            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            st.subheader("Atendimentos Agendados para Hoje")

            if apps_hoje:
                for a in apps_hoje:
                    with st.container(border=True):
                        c1, c2, c3 = st.columns([3, 2, 2])
                        c1.markdown(f"#### {a.get('servico_titulo', 'Serviço')}")
                        c1.caption(f"Duração: {a.get('duracao_minutos')} min")
                        c2.markdown(f"**Horário:** às **{a.get('hora_inicio')}**")
                        c2.markdown(f"**Valor:** {ui_utils.format_currency_brl(a.get('valor_cobrado', 0))}")
                        with c3:
                            st.markdown(ui_utils.status_badge_html(a.get('status')), unsafe_allow_html=True)
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "",
                        "Você ainda não tem agendamentos hoje",
                        "Quando seus clientes reservarem atendimentos para a data de hoje, eles aparecerão detalhados aqui com opções de confirmação e conclusão."
                    ),
                    unsafe_allow_html=True
                )

        # ---------------------------------------------------------------------
        # Aba 2: Agenda de Atendimentos
        # ---------------------------------------------------------------------
        with tab_agenda:
            st.subheader("Gestão de Atendimentos e Horários")
            st.markdown("Consulte e gerencie o ciclo de vida das reservas feitas pelos seus clientes.")

            suc_apps_agenda, todos_apps = appointment_service.get_appointments_by_user(user.get("id", 0), role="prestador", token=st.session_state.get("auth_token"))

            col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
            with col_f1:
                filtro_status = st.selectbox(
                    "Filtrar por Status",
                    options=["Todos", "confirmado", "pendente", "concluido", "cancelado"],
                    format_func=lambda s: "Todos os Status" if s == "Todos" else s.capitalize(),
                    key="prestador_filtro_status"
                )
            with col_f2:
                filtro_data = st.date_input(
                    "Filtrar por Data (opcional)",
                    value=None,
                    key="prestador_filtro_data"
                )

            apps_filtrados = todos_apps or []
            if filtro_status != "Todos":
                apps_filtrados = [a for a in apps_filtrados if ui_utils.normalize_status(a.get("status")) == ui_utils.normalize_status(filtro_status)]
            if filtro_data:
                data_str_f = filtro_data.strftime("%Y-%m-%d")
                apps_filtrados = [a for a in apps_filtrados if a.get("data") == data_str_f]

            with col_f3:
                st.markdown("<div style='margin-top: 1.7rem;'></div>", unsafe_allow_html=True)
                csv_data = ui_utils.generate_appointments_csv(apps_filtrados)
                st.download_button(
                    label="Exportar Agenda (CSV)",
                    data=csv_data,
                    file_name=f"agenda_atendimentos_{date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    disabled=len(apps_filtrados) == 0,
                    use_container_width=True,
                    help="Baixe a lista de atendimentos filtrados em formato compatível com Excel e planilhas."
                )

            if apps_filtrados:
                for a in apps_filtrados:
                    with st.container(border=True):
                        c_h1, c_h2, c_h3 = st.columns([3, 2, 2])
                        c_h1.markdown(f"#### {a.get('servico_titulo', 'Serviço')}")
                        data_br = ui_utils.format_date_short_pt_br(a.get('data'))
                        c_h2.markdown(f"**Data:** {data_br} às **{a.get('hora_inicio')}**")
                        
                        with c_h3:
                            st.markdown(ui_utils.status_badge_html(a.get("status")), unsafe_allow_html=True)

                        c_det1, c_det2, c_det3 = st.columns([3, 2, 2])
                        nome_cli_exib = a.get("cliente_nome") or "Cliente"
                        c_det1.caption(f"{nome_cli_exib} • Duração: {a.get('duracao_minutos')} min")

                        # Ação de WhatsApp para confirmação ou lembrete
                        tel_cli = a.get("cliente_telefone") or a.get("phone") or a.get("telefone") or ""
                        wa_url = ui_utils.get_whatsapp_link(
                            phone=tel_cli,
                            cliente_nome=nome_cli_exib,
                            servico_titulo=a.get("servico_titulo"),
                            data_str=a.get("data"),
                            hora_str=a.get("hora_inicio")
                        )
                        if wa_url:
                            c_det1.markdown(f"[Enviar Lembrete no WhatsApp]({wa_url})")
                        elif tel_cli:
                            c_det1.caption(f"Telefone: {tel_cli}")

                        valor_formatado = ui_utils.format_currency_brl(a.get('valor_cobrado', 0))
                        c_det2.markdown(f"**{valor_formatado}**")

                        with c_det3:
                            st_val = ui_utils.normalize_status(a.get("status"))
                            if st_val in ("confirmado", "pendente"):
                                col_b1, col_b2 = st.columns(2)
                                with col_b1:
                                    if st.button("Concluir", key=f"btn_concluir_{a.get('id')}", use_container_width=True):
                                        with st.spinner("Atualizando atendimento..."):
                                            appointment_service.update_appointment_status(a.get("id"), "concluido", token=st.session_state.get("auth_token"))
                                        st.toast("Atendimento marcado como concluído com sucesso.")
                                        st.rerun()
                                    with col_b2:
                                        if st.button("Cancelar", key=f"btn_cancel_prest_{a.get('id')}", use_container_width=True, type="secondary"):
                                            with st.spinner("Cancelando agendamento..."):
                                                appointment_service.update_appointment_status(a.get("id"), "cancelado", token=st.session_state.get("auth_token"))
                                            st.toast("Agendamento cancelado com sucesso.")
                                            st.rerun()
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "",
                        "Nenhum agendamento encontrado",
                        "Não há atendimentos para os filtros selecionados. Tente ajustar o status ou a data desejada."
                    ),
                    unsafe_allow_html=True
                )

        # ---------------------------------------------------------------------
        # Aba 3: Meus Serviços
        # ---------------------------------------------------------------------
        with tab_catalogo:
            st.subheader("Catálogo de Serviços")
            st.markdown("Gerencie os serviços oferecidos aos seus clientes com preços e tempos de duração.")

            with st.expander("Adicionar Novo Serviço", expanded=False):
                with st.form("form_new_service"):
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        titulo = st.text_input("Título do Serviço", placeholder="Ex: Corte Degradê")
                        preco = st.number_input("Preço (R$)", min_value=0.0, step=5.0, format="%.2f")
                    with col_s2:
                        duracao = st.number_input("Duração (minutos)", min_value=15, step=15)
                        descricao = st.text_input("Breve descrição (Opcional)", placeholder="Ex: Corte com acabamento na navalha")

                    submit_service = st.form_submit_button("Salvar Serviço no Catálogo", type="primary")
                    if submit_service:
                        if not titulo or not titulo.strip():
                            st.error("O título do serviço é obrigatório!")
                        elif preco <= 0:
                            st.error("O preço deve ser superior a R$ 0,00.")
                        else:
                            with st.spinner("Salvando serviço..."):
                                suc, msg = catalog_service.create_service(
                                    prestador_id=user.get("id", 0),
                                    titulo=titulo.strip(),
                                    preco=preco,
                                    duracao_minutos=duracao,
                                    descricao=descricao.strip(),
                                    token=st.session_state.get("auth_token")
                                )
                            if suc:
                                st.toast("Serviço adicionado com sucesso.")
                                st.rerun()
                            else:
                                st.error("Não foi possível adicionar o serviço. Verifique a conexão.")

            st.markdown("### Seus serviços cadastrados")
            if sucesso_cat and servicos:
                for s in servicos:
                    with st.container(border=True):
                        c_t1, c_t2 = st.columns([5, 2])
                        with c_t1:
                            st.markdown(f"**{s['titulo']}**")
                            if s.get('descricao'):
                                st.caption(f"{s['descricao']}")
                        with c_t2:
                            if s.get('ativo'):
                                st.markdown('<span style="display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; color:#047857; background:#ECFDF5; border:1px solid #A7F3D0;">Ativo</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span style="display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; color:#B91C1C; background:#FEF2F2; border:1px solid #FECACA;">Inativo</span>', unsafe_allow_html=True)

                        col_i1, col_i2, col_i3 = st.columns([2, 2, 3])
                        col_i1.markdown(f"**{ui_utils.format_currency_brl(s['preco'])}**")
                        col_i2.markdown(f"**{s['duracao_minutos']} min**")

                        with col_i3:
                            if s.get('ativo'):
                                if st.button("Desativar", key=f"desativar_{s['id']}", type="secondary", use_container_width=True):
                                    with st.spinner("Desativando serviço..."):
                                        suc_t, _ = catalog_service.toggle_service_status(s["id"], False, st.session_state.get("auth_token"))
                                    if suc_t:
                                        st.toast("Serviço desativado com sucesso.")
                                        st.rerun()
                                    else:
                                        st.error("Não foi possível desativar o serviço.")
                            else:
                                if st.button("Reativar", key=f"reativar_{s['id']}", type="primary", use_container_width=True):
                                    with st.spinner("Reativando serviço..."):
                                        suc_t, _ = catalog_service.toggle_service_status(s["id"], True, st.session_state.get("auth_token"))
                                    if suc_t:
                                        st.toast("Serviço reativado com sucesso.")
                                        st.rerun()
                                    else:
                                        st.error("Não foi possível reativar o serviço.")
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "",
                        "Nenhum serviço cadastrado ainda",
                        "Cadastre seu primeiro serviço utilizando o botão 'Adicionar Novo Serviço' acima para disponibilizar seus atendimentos aos clientes."
                    ),
                    unsafe_allow_html=True
                )

        # ---------------------------------------------------------------------
        # Aba 4: Grade de Atendimento
        # ---------------------------------------------------------------------
        with tab_grade:
            st.subheader("Configuração da Grade de Atendimento")
            st.markdown("Defina os dias da semana e os horários em que você atende seus clientes.")

            suc_grade, grade_atual = availability_service.get_availability(user.get("id", 0), st.session_state.get("auth_token"))
            if not grade_atual:
                grade_atual = [
                    {"dia_semana": i, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": (1 <= i <= 5)}
                    for i in range(7)
                ]

            dias_nome = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
            nova_grade = []

            with st.form("form_grade_atendimento"):
                def str_to_time(t_str):
                    if not t_str:
                        return None
                    try:
                        h, m = map(int, t_str.split(':')[:2])
                        return time(h, m)
                    except Exception:
                        return None

                for dia_idx in range(7):
                    dados_dia = next((d for d in grade_atual if d["dia_semana"] == dia_idx), None)
                    if not dados_dia:
                        dados_dia = {"dia_semana": dia_idx, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": False}

                    st.markdown(f"#### {dias_nome[dia_idx]}")
                    col_ativo, col_ini, col_fim, col_int_ini, col_int_fim = st.columns(5)

                    ativo = col_ativo.checkbox("Atender neste dia", value=dados_dia.get("ativo", False), key=f"ativo_{dia_idx}")

                    h_ini = str_to_time(dados_dia.get("hora_inicio")) or time(9, 0)
                    h_fim = str_to_time(dados_dia.get("hora_fim")) or time(18, 0)
                    int_ini = str_to_time(dados_dia.get("intervalo_inicio")) or time(12, 0)
                    int_fim = str_to_time(dados_dia.get("intervalo_fim")) or time(13, 0)
                    has_pausa = col_ativo.checkbox("Intervalo / Almoço", value=bool(dados_dia.get("intervalo_inicio")), key=f"tem_pausa_{dia_idx}", disabled=not ativo)

                    t_ini = col_ini.time_input("Início", value=h_ini, key=f"ini_{dia_idx}", disabled=not ativo)
                    t_fim = col_fim.time_input("Término", value=h_fim, key=f"fim_{dia_idx}", disabled=not ativo)
                    t_int_ini = col_int_ini.time_input("Pausa (Início)", value=int_ini, key=f"int_ini_{dia_idx}", disabled=(not ativo or not has_pausa))
                    t_int_fim = col_int_fim.time_input("Pausa (Fim)", value=int_fim, key=f"int_fim_{dia_idx}", disabled=(not ativo or not has_pausa))

                    nova_grade.append({
                        "dia_semana": dia_idx,
                        "ativo": ativo,
                        "hora_inicio": t_ini.strftime("%H:%M") if t_ini else None,
                        "hora_fim": t_fim.strftime("%H:%M") if t_fim else None,
                        "intervalo_inicio": t_int_ini.strftime("%H:%M") if (t_int_ini and has_pausa) else None,
                        "intervalo_fim": t_int_fim.strftime("%H:%M") if (t_int_fim and has_pausa) else None
                    })
                    st.markdown("<hr style='margin:0.5rem 0 1rem 0; border-color:#E2E8F0;'>", unsafe_allow_html=True)

                submit_grade = st.form_submit_button("Salvar Grade de Atendimento", type="primary", use_container_width=True)

                if submit_grade:
                    has_error = False
                    for d in nova_grade:
                        if d["ativo"]:
                            h_in = d["hora_inicio"]
                            h_fi = d["hora_fim"]
                            if h_in and h_fi and h_in >= h_fi:
                                st.error(f"Erro em {dias_nome[d['dia_semana']]}: O horário de término deve ser posterior ao início.")
                                has_error = True

                            p_in = d["intervalo_inicio"]
                            p_fi = d["intervalo_fim"]
                            if p_in and p_fi:
                                if p_in >= p_fi:
                                    st.error(f"Erro em {dias_nome[d['dia_semana']]}: O término da pausa deve ser posterior ao início.")
                                    has_error = True
                                if p_in < h_in or p_fi > h_fi:
                                    st.error(f"Erro em {dias_nome[d['dia_semana']]}: A pausa deve estar contida dentro do horário de expediente.")
                                    has_error = True

                    if not has_error:
                        with st.spinner("Salvando disponibilidade..."):
                            suc, msg = availability_service.save_availability(user.get("id", 0), nova_grade, st.session_state.get("auth_token"))
                        if suc:
                            st.toast("Grade de horários salva com sucesso.")
                            st.success("Sua grade de atendimento foi atualizada com sucesso.")
                        else:
                            st.error("Não foi possível salvar a grade de atendimento.")


    # =========================================================================
    # VISÃO DO CLIENTE
    # =========================================================================
    else:
        nome_cliente = user.get('name', 'Cliente')
        data_formatada = ui_utils.format_date_long_pt_br()

        st.markdown(
            f'<div style="margin-bottom:1.5rem;">'
            f'<div style="font-size:2rem; font-weight:800; color:#0F172A; margin-bottom:0.25rem;">Olá, {nome_cliente}!</div>'
            f'<div style="font-size:0.95rem; color:#64748B; display:flex; align-items:center; gap:8px;">'
            f'<span>Área do Cliente</span><span>•</span><span>{data_formatada}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        suc_c_apps, cliente_apps = appointment_service.get_appointments_by_user(user.get("id", 0), role="cliente", token=st.session_state.get("auth_token"))
        cliente_apps = cliente_apps or []
        apps_ativos = [a for a in cliente_apps if ui_utils.normalize_status(a.get("status")) in ("confirmado", "pendente")]
        apps_passados = [a for a in cliente_apps if ui_utils.normalize_status(a.get("status")) in ("concluido", "cancelado")]

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(ui_utils.metric_card_html("Agendamentos Ativos", str(len(apps_ativos)), "Próximos atendimentos"), unsafe_allow_html=True)
        with col_c2:
            st.markdown(ui_utils.metric_card_html("Total de Agendamentos", str(len(cliente_apps)), f"{len(apps_passados)} concluído(s) ou cancelado(s)"), unsafe_allow_html=True)

        # Verificação contextual de atendimento concluído pendente de avaliação
        apps_pendentes_avaliacao = [
            a for a in cliente_apps
            if ui_utils.normalize_status(a.get("status")) == "concluido" and not review_service.is_appointment_reviewed(a.get("id"), token=st.session_state.get("auth_token"))
        ]
        if apps_pendentes_avaliacao:
            primeiro_pendente = apps_pendentes_avaliacao[0]
            p_id_pend = primeiro_pendente.get("id")
            # Se ainda não dispensou nesta interação e não abriu modal agora, exibe banner com lembrete persistente
            st.info(f"✨ Você tem um atendimento recente de **{primeiro_pendente.get('servico_titulo', 'Serviço')}** aguardando sua avaliação! Sua opinião ajuda a melhorar nossos serviços.")
            if not st.session_state.get(f"dismissed_review_dialog_{p_id_pend}") and not st.session_state.get("review_dialog_shown"):
                st.session_state["review_dialog_shown"] = True
                show_review_appointment_dialog(primeiro_pendente, user, token=st.session_state.get("auth_token"))

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        tab_cli_assistente, tab_cli_catalogo, tab_cli_agendamentos = st.tabs([
            "🤖 Assistente de Recomendação",
            "📖 Catálogo Geral",
            "🗓️ Meus Agendamentos"
        ])

        # ---------------------------------------------------------------------
        # Aba: Assistente Inteligente de Recomendação (Frente A)
        # ---------------------------------------------------------------------
        with tab_cli_assistente:
            st.markdown(ui_utils.section_header_html(
                "Assistente Inteligente de Recomendação",
                "Encontre os profissionais mais recomendados para sua necessidade, com base em compatibilidade de serviços, orçamento e horários disponíveis."
            ), unsafe_allow_html=True)

            with st.form("form_smart_recommendation"):
                col_rec1, col_rec2 = st.columns(2)
                with col_rec1:
                    rec_termo = st.text_input("Qual serviço você procura?", placeholder="Ex: Corte de Cabelo, Barba, Massagem...")
                    rec_desc = st.text_area("Descreva brevemente sua necessidade (opcional)", placeholder="Ex: Preciso de corte degradê bem alinhado antes das 18h", height=85)
                with col_rec2:
                    rec_orcamento = st.number_input("Orçamento Máximo (R$)", min_value=0.0, value=80.0, step=10.0, format="%.2f", help="Prestadores acima deste valor não serão apresentados.")
                    rec_data = st.date_input("Data pretendida para o atendimento", min_value=date.today(), value=date.today(), help="Apenas prestadores com vagas livres nesta data serão considerados.")

                submit_rec = st.form_submit_button("Encontrar Melhores Recomendações", type="primary", use_container_width=True)

            if submit_rec or st.session_state.get("rec_has_searched"):
                if submit_rec:
                    st.session_state["rec_has_searched"] = True
                    st.session_state["rec_termo_s"] = rec_termo
                    st.session_state["rec_desc_s"] = rec_desc
                    st.session_state["rec_orc_s"] = rec_orcamento
                    st.session_state["rec_data_s"] = rec_data

                termo_s = st.session_state.get("rec_termo_s", "")
                desc_s = st.session_state.get("rec_desc_s", "")
                orc_s = st.session_state.get("rec_orc_s", 0.0)
                dt_s = st.session_state.get("rec_data_s", date.today())
                dt_str_s = dt_s.strftime("%Y-%m-%d")

                with st.spinner("Analisando especialidades, verificando vagas livres e calculando scores..."):
                    recs = recommendation_service.recommend_providers(
                        termo_busca=termo_s,
                        descricao_necessidade=desc_s,
                        orcamento_max=orc_s,
                        data_str=dt_str_s,
                        token=st.session_state.get("auth_token")
                    )

                if recs:
                    st.markdown(f"#### Encontramos **{len(recs)}** profissional(is) compatível(is) para {ui_utils.format_date_short_pt_br(dt_s)}:")
                    for idx, item in enumerate(recs):
                        serv_item = item["servico"]
                        p_id = item["prestador_id"]
                        p_nome = item["prestador_nome"]
                        score = item["score"]
                        justificativas = item["justificativas"]
                        slots = item["slots_disponiveis"]
                        breakdown = item["score_breakdown"]
                        preco_brl = ui_utils.format_currency_brl(serv_item.get("preco", 0))

                        with st.container(border=True):
                            c_top1, c_top2 = st.columns([3, 1])
                            with c_top1:
                                st.markdown(f"### {serv_item.get('titulo')} — *{p_nome}*")
                                if serv_item.get("descricao"):
                                    st.caption(serv_item.get("descricao"))
                            with c_top2:
                                st.markdown(ui_utils.recommendation_badge_html(score), unsafe_allow_html=True)

                            col_d1, col_d2 = st.columns([1, 2])
                            with col_d1:
                                st.markdown(f"**Preço:** {preco_brl}")
                                st.markdown(f"**Duração:** {serv_item.get('duracao_minutos', 30)} min")
                                st.markdown(f"**Data:** {ui_utils.format_date_short_pt_br(dt_s)}")
                            with col_d2:
                                st.markdown("**Fatores da Recomendação:**")
                                for just in justificativas:
                                    st.markdown(f"- {just}")

                            # Média das avaliações do serviço
                            m_serv_rec = review_service.get_metrics(servico_id=serv_item.get('id'), token=st.session_state.get("auth_token"))
                            with st.expander("Média das avaliações", expanded=False):
                                st.markdown(ui_utils.service_reviews_summary_html(m_serv_rec["nota_media"], m_serv_rec["total_avaliacoes"]), unsafe_allow_html=True)

                            # Atalho para Agendamento Imediato
                            with st.expander(f"Reservar Horário com {p_nome}", expanded=False):
                                if slots:
                                    slot_escolhido = st.selectbox(
                                        "Horários disponíveis confirmados no dia:",
                                        options=slots,
                                        key=f"slot_rec_{serv_item.get('id')}_{idx}"
                                    )
                                    if st.button("Confirmar Agendamento Imediato", key=f"btn_rec_{serv_item.get('id')}_{idx}", type="primary", use_container_width=True):
                                        with st.spinner("Confirmando agendamento..."):
                                            suc_rec, resp_rec = appointment_service.create_appointment(
                                                cliente_id=user.get("id", 0),
                                                prestador_id=p_id,
                                                servico_id=serv_item.get("id"),
                                                data_str=dt_str_s,
                                                hora_inicio=slot_escolhido,
                                                token=st.session_state.get("auth_token"),
                                                cliente_nome=user.get("name"),
                                                cliente_telefone=user.get("phone")
                                            )
                                        if suc_rec:
                                            st.toast("Agendamento confirmado com sucesso.")
                                            st.success(f"Agendamento confirmado para {ui_utils.format_date_short_pt_br(dt_s)} às {slot_escolhido}!")
                                            st.rerun()
                                        else:
                                            st.error(f"{resp_rec.get('message', 'Erro ao agendar.')}")
                                else:
                                    st.warning("Nenhum horário livre disponível no momento.")
                else:
                    st.markdown(ui_utils.empty_state_html(
                        "",
                        "Nenhum profissional elegível para esta pesquisa",
                        f"Não encontramos prestadores com serviço compatível, orçamento até {ui_utils.format_currency_brl(orc_s)} e com horários livres em {ui_utils.format_date_short_pt_br(dt_s)}. Tente flexibilizar a data ou aumentar o orçamento máximo."
                    ), unsafe_allow_html=True)

        with tab_cli_catalogo:
            st.subheader("Catálogo de Serviços Disponíveis")
            st.markdown("Escolha um serviço abaixo, selecione a data e o horário desejado para agendar.")

            suc_pub, servicos_pub = catalog_service.get_public_services(token=st.session_state.get("auth_token"))
            if suc_pub and servicos_pub:
                cols = st.columns(2)
                for idx, serv in enumerate(servicos_pub):
                    with cols[idx % 2]:
                        with st.container(border=True):
                            st.markdown(f"#### {serv.get('titulo')}")
                            if serv.get("descricao"):
                                st.write(serv.get("descricao"))
                            c_a, c_b = st.columns(2)
                            c_a.markdown(f"**Valor:** {ui_utils.format_currency_brl(serv.get('preco', 0))}")
                            c_b.markdown(f"**Duração:** {serv.get('duracao_minutos')} min")

                            s_id = serv.get("id")
                            p_id = serv.get("prestador_id", 15)
                            dur_min = serv.get("duracao_minutos", 30)
                            st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)
                            col_act1, col_act2 = st.columns(2)
                            with col_act1:
                                if st.button("Detalhes", key=f"btn_detalhes_{s_id}", use_container_width=True):
                                    show_service_details_dialog(serv, token=st.session_state.get("auth_token"), user=user)
                            with col_act2:
                                with st.popover("Selecionar Horário e Agendar", use_container_width=True):
                                    st.markdown(f"#### Agendar: {serv.get('titulo')}")
                                    st.caption(f"Duração: {dur_min} min | Valor: {ui_utils.format_currency_brl(serv.get('preco', 0))}")

                                    dt_escolhida = st.date_input(
                                        "Data do Atendimento",
                                        min_value=date.today(),
                                        value=date.today(),
                                        key=f"cli_date_{s_id}"
                                    )
                                    dt_escolhida_str = dt_escolhida.strftime("%Y-%m-%d")

                                    slots_livres = appointment_service.calculate_available_slots(
                                        prestador_id=p_id,
                                        date_str=dt_escolhida_str,
                                        duration_minutes=dur_min,
                                        token=st.session_state.get("auth_token")
                                    )

                                    if slots_livres:
                                        slot_selecionado = st.selectbox(
                                            "Horários livres disponíveis:",
                                            options=slots_livres,
                                            key=f"cli_slot_{s_id}"
                                        )
                                        if st.button("Confirmar Agendamento", key=f"btn_confirmar_{s_id}", type="primary", use_container_width=True):
                                            with st.spinner("Confirmando agendamento..."):
                                                suc_ag, resp_ag = appointment_service.create_appointment(
                                                    cliente_id=user.get("id", 0),
                                                    prestador_id=p_id,
                                                    servico_id=s_id,
                                                    data_str=dt_escolhida_str,
                                                    hora_inicio=slot_selecionado,
                                                    token=st.session_state.get("auth_token"),
                                                    cliente_nome=user.get("name"),
                                                    cliente_telefone=user.get("phone")
                                                )
                                            if suc_ag:
                                                st.toast("Agendamento confirmado com sucesso.")
                                                st.success(f"Agendamento confirmado para {ui_utils.format_date_short_pt_br(dt_escolhida)} às {slot_selecionado}!")
                                                st.rerun()
                                            else:
                                                st.error(f"{resp_ag.get('message', 'Erro ao agendar.')}")
                                    else:
                                        st.warning("Nenhum horário livre disponível para esta data.")
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "",
                        "Nenhum serviço ativo disponível",
                        "No momento não há serviços disponíveis para agendamento no catálogo."
                    ),
                    unsafe_allow_html=True
                )

        with tab_cli_agendamentos:
            st.subheader("Seus Agendamentos Realizados")
            st.markdown("Consulte seus atendimentos programados e histórico de agendamentos.")

            if cliente_apps:
                for app in cliente_apps:
                    with st.container(border=True):
                        col_a1, col_a2, col_a3 = st.columns([3, 2, 2])
                        col_a1.markdown(f"#### {app.get('servico_titulo', 'Serviço')}")
                        data_cli_br = ui_utils.format_date_short_pt_br(app.get('data'))
                        col_a2.markdown(f"**Data:** {data_cli_br} às **{app.get('hora_inicio')}**")
                        with col_a3:
                            st.markdown(ui_utils.status_badge_html(app.get("status")), unsafe_allow_html=True)

                        col_sub1, col_sub2, col_sub3 = st.columns([3, 2, 2])
                        col_sub1.caption(f"Duração: {app.get('duracao_minutos')} min")
                        col_sub2.markdown(f"**{ui_utils.format_currency_brl(app.get('valor_cobrado', 0))}**")

                        with col_sub3:
                            st_app = ui_utils.normalize_status(app.get("status"))
                            if st_app in ("confirmado", "pendente"):
                                if st.button("Cancelar Agendamento", key=f"btn_cancel_cli_{app.get('id')}", use_container_width=True, type="secondary"):
                                    with st.spinner("Cancelando..."):
                                        appointment_service.update_appointment_status(app.get("id"), "cancelado", token=st.session_state.get("auth_token"))
                                    st.toast("Agendamento cancelado com sucesso.")
                                    st.rerun()
                            elif st_app == "concluido":
                                app_id = app.get("id")
                                ja_avaliado = review_service.is_appointment_reviewed(app_id, token=st.session_state.get("auth_token"))
                                if ja_avaliado:
                                    rev = review_service.get_review_by_appointment(app_id, token=st.session_state.get("auth_token"))
                                    nota_rev = rev.get("nota", 5) if rev else 5
                                    st.markdown(
                                        f'<span style="display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700; color:#047857; background:#ECFDF5; border:1px solid #A7F3D0;">★ Avaliado ({nota_rev}/5)</span>',
                                        unsafe_allow_html=True
                                    )
                                else:
                                    if st.button("Avaliar Atendimento", key=f"btn_avaliar_dlg_{app_id}", type="primary", use_container_width=True):
                                        show_review_appointment_dialog(app, user, token=st.session_state.get("auth_token"))
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "",
                        "Você ainda não possui nenhum agendamento realizado",
                        "Acesse a aba 'Catálogo & Agendamento' para escolher um serviço e marcar seu primeiro atendimento."
                    ),
                    unsafe_allow_html=True
                )
