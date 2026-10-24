"""
AgendAí — Plataforma de Gestão e Agendamento para Prestadores Independentes
Frontend principal desenvolvido em Streamlit conectado ao backend Xano.
"""

import streamlit as st
from datetime import date, datetime, time
from services import (
    auth_service,
    api_client,
    catalog_service,
    availability_service,
    appointment_service,
    ui_utils
)

st.set_page_config(
    page_title="AgendAí — Gestão e Agendamento",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom CSS (Plataforma Dark Theme Profissional)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Tipografia e Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
    }

    /* Container e Cabeçalho */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }

    /* Cards e Formulários com Dark Glassmorphism */
    div[data-testid="stForm"] {
        background: #111827;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Inputs Escuros e Estilizados */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
        background-color: #1E293B !important;
    }

    /* Botões Primários com Gradiente */
    div[data-testid="stForm"] button[kind="primary"], button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.25rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    div[data-testid="stForm"] button[kind="primary"]:hover, button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.55) !important;
    }

    /* Botões Secundários */
    button[kind="secondary"] {
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        background-color: #334155 !important;
        border-color: #475569 !important;
        color: #FFFFFF !important;
    }

    /* Tabs Customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #94A3B8 !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1E293B !important;
        color: #60A5FA !important;
    }

    /* Limpeza de elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

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


def do_logout():
    """Limpa os dados de autenticação e encerra a sessão com redirecionamento limpo."""
    st.session_state["authenticated"] = False
    st.session_state["auth_token"] = None
    st.session_state["user"] = None
    st.session_state["show_recovery"] = False
    st.rerun()


# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:1.2rem;">
        <span style="font-size:2rem;">📅</span>
        <div>
            <div style="font-size:1.35rem; font-weight:800; color:#F8FAFC; line-height:1.1;">AgendAí</div>
            <div style="font-size:0.75rem; color:#94A3B8;">Innovation Lab • Impacta</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["authenticated"]:
        user = st.session_state["user"]
        role = user.get("role", "cliente")
        initials = ui_utils.get_initials(user.get("name", "Usuário"))
        role_label = "✂️ Prestador Autônomo" if role == "prestador" else "📱 Cliente"
        badge_style = (
            "background:rgba(59,130,246,0.15); color:#60A5FA; border:1px solid rgba(59,130,246,0.3);"
            if role == "prestador"
            else "background:rgba(16,185,129,0.15); color:#34D399; border:1px solid rgba(16,185,129,0.3);"
        )

        st.markdown(f"""
        <div style="background:#111827; border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:1.2rem; margin-bottom:1.2rem; box-shadow:0 4px 12px rgba(0,0,0,0.3);">
            <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:8px;">Perfil Ativo</div>
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                <div style="width:44px; height:44px; border-radius:50%; background:linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.05rem; color:#FFFFFF; box-shadow:0 4px 10px rgba(59,130,246,0.35); flex-shrink:0;">
                    {initials}
                </div>
                <div style="overflow:hidden;">
                    <div style="font-size:1rem; font-weight:700; color:#F8FAFC; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user.get('name', 'Usuário')}</div>
                    <div style="font-size:0.75rem; color:#94A3B8; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user.get('email', '')}</div>
                </div>
            </div>
            <span style="display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; {badge_style}">
                {role_label}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sair", use_container_width=True, type="secondary"):
            do_logout()
    else:
        st.info("🔒 Faça login ou crie sua conta para acessar o AgendAí.")

    st.markdown("---")
    with st.expander("⚙️ Conexão & Resiliência"):
        api_url = api_client.API_BASE_URL
        is_placeholder = api_client.is_placeholder_url(api_url)
        if is_placeholder:
            st.warning("⚠️ Modo Local Simulado ativo.")
        else:
            st.success(f"🟢 Backend Xano: `{api_url}`")
            st.caption("🛡️ Camada de Resiliência ativa: tolerância a falhas e respostas nulas garantem continuidade operacional.")


# -----------------------------------------------------------------------------
# Interface Principal: Não Autenticado (Login / Cadastro)
# -----------------------------------------------------------------------------
if not st.session_state["authenticated"]:
    st.markdown('<div class="hero-title">Bem-vindo ao AgendAí 📅</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Plataforma inteligente de gestão e agendamento que elimina o atrito de atendimento manual para prestadores autônomos e seus clientes.</div>',
        unsafe_allow_html=True
    )

    tab_login, tab_signup, tab_about = st.tabs(["🔑 Entrar", "📝 Criar Conta", "ℹ️ Sobre o Projeto"])

    # Aba: Login
    with tab_login:
        st.subheader("Acesse sua conta")
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
                    st.toast("Login realizado com sucesso! 🎉")
                    st.rerun()
                else:
                    st.error(f"❌ {response.get('message', 'Erro ao efetuar login.')}")

        if not st.session_state.get("show_recovery"):
            if st.button("🔐 Esqueceu sua senha? Clique aqui para recuperar", use_container_width=True):
                st.session_state["show_recovery"] = True
                st.rerun()
        else:
            st.markdown("---")
            st.info("Preencha seu e-mail cadastrado abaixo para receber as instruções de recuperação de senha.")
            with st.form("form_recovery"):
                email_recovery = st.text_input("E-mail cadastrado", placeholder="seu.email@exemplo.com")
                submit_recovery = st.form_submit_button("Enviar instruções de recuperação", use_container_width=True, type="primary")
                if submit_recovery:
                    with st.spinner("Enviando instruções..."):
                        success, msg = auth_service.recover_password(email_recovery)
                    if success:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")

            if st.button("⬅️ Voltar para o Login", use_container_width=True):
                st.session_state["show_recovery"] = False
                st.rerun()

        st.markdown("---")
        st.markdown("#### ⚡ Acesso Rápido para Demonstração:")
        col_demo1, col_demo2 = st.columns(2)
        with col_demo1:
            if st.button("✂️ Entrar como Prestador (Hector Barros)", use_container_width=True):
                # Tenta autenticação no Xano ou inicia sessão direta para Hector Barros
                suc_h, resp_h = auth_service.login("hector.barros@aluno.impacta.edu.br", "123")
                if not suc_h:
                    resp_h = {
                        "authToken": "jwt_session_15_prestador",
                        "user": {
                            "id": 15,
                            "name": "Hector Barros",
                            "email": "hector.barros@aluno.impacta.edu.br",
                            "role": "prestador",
                            "phone": "11989898768",
                            "account_id": 0
                        }
                    }
                st.session_state["authenticated"] = True
                st.session_state["auth_token"] = resp_h.get("authToken")
                st.session_state["user"] = resp_h.get("user")
                st.toast("Bem-vindo de volta, Hector! ✂️")
                st.rerun()
        with col_demo2:
            st.info("💡 Para testar o **cadastro de clientes do zero**, clique na aba **'📝 Criar Conta'** acima!")

    # Aba: Cadastro
    with tab_signup:
        st.subheader("Crie sua conta no AgendAí")
        with st.form("form_signup"):
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                name_signup = st.text_input("Nome Completo / Nome Fantasia", placeholder="Ex: Lucas Ferreira")
                email_signup = st.text_input("E-mail", placeholder="exemplo@email.com")
            with col_u2:
                phone_signup = st.text_input("WhatsApp / Telefone", placeholder="(11) 99999-9999")
                pass_signup = st.text_input("Senha", type="password", placeholder="Mínimo 8 caracteres (com letras e números)")

            role_choice = st.radio(
                "Qual é o seu perfil de uso?",
                options=["prestador", "cliente"],
                format_func=lambda r: "✂️ Prestador de Serviços (quero divulgar horários e gerenciar clientes)" if r == "prestador" else "📱 Cliente (quero agendar serviços com facilidade)",
                horizontal=False
            )

            submit_signup = st.form_submit_button("Cadastrar e Começar", use_container_width=True, type="primary")

            if submit_signup:
                with st.spinner("Criando sua conta..."):
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
                    st.toast("Conta criada com sucesso! 🎉")
                    st.rerun()
                else:
                    st.error(f"❌ {response.get('message', 'Erro ao criar conta.')}")

    # Aba: Sobre o Projeto
    with tab_about:
        st.markdown("""
        ### 🚀 Sobre a Engenharia do AgendAí
        - **Metodologia**: Spec-Driven Development (SDD) com governança **OpenSpec**.
        - **Backend**: **Xano** (APIs REST, XanoScript e PostgreSQL gerenciado).
        - **Frontend**: **Streamlit** (Python 3.14).
        - **Disciplina**: Innovation Lab: Advanced No/Low Code (Faculdade IMPACTA).
        """)

# -----------------------------------------------------------------------------
# Interface Principal: Usuário Autenticado
# -----------------------------------------------------------------------------
else:
    user = st.session_state["user"]
    role = user.get("role", "cliente")

    # =========================================================================
    # VISÃO DO PRESTADOR DE SERVIÇOS
    # =========================================================================
    if role == "prestador":
        # Cabeçalho do Prestador
        nome_prestador = user.get('name', 'Prestador')
        data_formatada = ui_utils.format_date_long_pt_br()

        st.markdown(f"""
        <div style="margin-bottom:1.5rem;">
            <div style="font-size:2rem; font-weight:800; color:#F8FAFC; margin-bottom:0.25rem;">
                Olá, {nome_prestador}! 👋
            </div>
            <div style="font-size:0.95rem; color:#94A3B8; display:flex; align-items:center; gap:8px;">
                <span>✂️ Painel do Prestador</span>
                <span>•</span>
                <span>🗓️ {data_formatada}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_resumo, tab_agenda, tab_catalogo, tab_grade = st.tabs([
            "📊 Resumo", "📅 Agenda de Atendimentos", "✂️ Meus Serviços", "🕒 Grade de Atendimento"
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
            apps_hoje = [a for a in prestador_apps if a.get("data") == today_str and a.get("status") in ("confirmado", "pendente", "concluido")] if prestador_apps else []
            receita_prevista = sum(float(a.get("valor_cobrado", 0)) for a in prestador_apps if a.get("status") in ("confirmado", "concluido")) if prestador_apps else 0.0

            # 3 Cards de Métricas Neutros e Profissionais
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                sub_hoje = f"{len(apps_hoje)} agendamento(s) para hoje" if len(apps_hoje) > 0 else "Nenhum agendamento para hoje"
                st.markdown(ui_utils.metric_card_html("Agendamentos Hoje", str(len(apps_hoje)), sub_hoje, "📅"), unsafe_allow_html=True)
            with col_m2:
                sub_ativos = "Disponíveis para clientes" if qtd_ativos > 0 else "Nenhum serviço ativo"
                st.markdown(ui_utils.metric_card_html("Serviços Ativos", str(qtd_ativos), sub_ativos, "✂️"), unsafe_allow_html=True)
            with col_m3:
                sub_preco = f"Receita prevista: {ui_utils.format_currency_brl(receita_prevista)}" if receita_prevista > 0 else "Base de serviços ativos"
                st.markdown(ui_utils.metric_card_html("Preço Médio", ui_utils.format_currency_brl(preco_medio), sub_preco, "💰"), unsafe_allow_html=True)

            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            st.subheader("📅 Atendimentos Agendados para Hoje")

            if apps_hoje:
                for a in apps_hoje:
                    with st.container(border=True):
                        c1, c2, c3 = st.columns([3, 2, 2])
                        c1.markdown(f"#### ✂️ {a.get('servico_titulo', 'Serviço')}")
                        c1.caption(f"⏱️ Duração: {a.get('duracao_minutos')} min | Agendamento #{a.get('id')}")
                        c2.markdown(f"🗓️ **Horário:** às **{a.get('hora_inicio')}**")
                        c2.markdown(f"💰 **Valor:** {ui_utils.format_currency_brl(a.get('valor_cobrado', 0))}")
                        with c3:
                            st.markdown(ui_utils.status_badge_html(a.get('status')), unsafe_allow_html=True)
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "📅",
                        "Você ainda não tem agendamentos hoje",
                        "Quando seus clientes reservarem atendimentos para a data de hoje, eles aparecerão detalhados aqui com opções de confirmação e conclusão."
                    ),
                    unsafe_allow_html=True
                )

        # ---------------------------------------------------------------------
        # Aba 2: Agenda de Atendimentos
        # ---------------------------------------------------------------------
        with tab_agenda:
            st.subheader("📅 Gestão de Atendimentos e Horários")
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
                apps_filtrados = [a for a in apps_filtrados if a.get("status") == filtro_status]
            if filtro_data:
                data_str_f = filtro_data.strftime("%Y-%m-%d")
                apps_filtrados = [a for a in apps_filtrados if a.get("data") == data_str_f]

            with col_f3:
                st.markdown("<div style='margin-top: 1.7rem;'></div>", unsafe_allow_html=True)
                csv_data = ui_utils.generate_appointments_csv(apps_filtrados)
                st.download_button(
                    label="📥 Exportar Agenda (CSV)",
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
                        c_h1.markdown(f"#### ✂️ {a.get('servico_titulo', 'Serviço')}")
                        data_br = ui_utils.format_date_short_pt_br(a.get('data'))
                        c_h2.markdown(f"🗓️ **Data:** {data_br} às **{a.get('hora_inicio')}**")
                        
                        with c_h3:
                            st.markdown(ui_utils.status_badge_html(a.get("status")), unsafe_allow_html=True)

                        c_det1, c_det2, c_det3 = st.columns([3, 2, 2])
                        nome_cli_exib = a.get("cliente_nome") or f"Cliente #{a.get('cliente_id')}"
                        c_det1.caption(f"👤 {nome_cli_exib} | ⏱️ Duração: {a.get('duracao_minutos')} min")

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
                            c_det1.markdown(f"[💬 Enviar Lembrete no WhatsApp]({wa_url})")
                        elif tel_cli:
                            c_det1.caption(f"📞 Telefone: {tel_cli}")

                        valor_formatado = ui_utils.format_currency_brl(a.get('valor_cobrado', 0))
                        c_det2.markdown(f"💰 **{valor_formatado}**")

                        with c_det3:
                            st_val = a.get("status")
                            if st_val in ("confirmado", "pendente"):
                                col_b1, col_b2 = st.columns(2)
                                with col_b1:
                                    if st.button("✅ Concluir", key=f"btn_concluir_{a.get('id')}", use_container_width=True):
                                        with st.spinner("Atualizando atendimento..."):
                                            appointment_service.update_appointment_status(a.get("id"), "concluido", token=st.session_state.get("auth_token"))
                                        st.toast("Atendimento marcado como concluído! 🎉")
                                        st.rerun()
                                with col_b2:
                                    if st.button("❌ Cancelar", key=f"btn_cancel_prest_{a.get('id')}", use_container_width=True, type="secondary"):
                                        with st.spinner("Cancelando agendamento..."):
                                            appointment_service.update_appointment_status(a.get("id"), "cancelado", token=st.session_state.get("auth_token"))
                                        st.toast("Agendamento cancelado.")
                                        st.rerun()
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "🗓️",
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

            with st.expander("➕ Adicionar Novo Serviço", expanded=False):
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
                                st.toast("Serviço adicionado com sucesso! 🎉")
                                st.rerun()
                            else:
                                st.error("Não foi possível adicionar o serviço. Verifique a conexão.")

            st.markdown("### Seus serviços cadastrados")
            if sucesso_cat and servicos:
                for s in servicos:
                    with st.container(border=True):
                        c_t1, c_t2 = st.columns([5, 2])
                        with c_t1:
                            st.markdown(f"**✂️ {s['titulo']}**")
                            if s.get('descricao'):
                                st.caption(f"{s['descricao']}")
                        with c_t2:
                            if s.get('ativo'):
                                st.markdown('<span style="display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; color:#10B981; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3);">Ativo</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span style="display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; color:#EF4444; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.3);">Inativo</span>', unsafe_allow_html=True)

                        col_i1, col_i2, col_i3 = st.columns([2, 2, 3])
                        col_i1.markdown(f"💰 **{ui_utils.format_currency_brl(s['preco'])}**")
                        col_i2.markdown(f"⏱️ **{s['duracao_minutos']} min**")

                        with col_i3:
                            if s.get('ativo'):
                                if st.button("Desativar", key=f"desativar_{s['id']}", type="secondary", use_container_width=True):
                                    with st.spinner("Atualizando..."):
                                        catalog_service.toggle_service_status(s["id"], False, st.session_state.get("auth_token"))
                                    st.toast("Serviço desativado.")
                                    st.rerun()
                            else:
                                if st.button("Reativar", key=f"reativar_{s['id']}", type="primary", use_container_width=True):
                                    with st.spinner("Atualizando..."):
                                        catalog_service.toggle_service_status(s["id"], True, st.session_state.get("auth_token"))
                                    st.toast("Serviço reativado! ✂️")
                                    st.rerun()
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "✂️",
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

                    st.markdown(f"#### 🗓️ {dias_nome[dia_idx]}")
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
                    st.markdown("<hr style='margin:0.5rem 0 1rem 0; border-color:#1E293B;'>", unsafe_allow_html=True)

                submit_grade = st.form_submit_button("Salvar Grade de Atendimento", type="primary", use_container_width=True)

                if submit_grade:
                    has_error = False
                    for d in nova_grade:
                        if d["ativo"]:
                            h_in = d["hora_inicio"]
                            h_fi = d["hora_fim"]
                            if h_in and h_fi and h_in >= h_fi:
                                st.error(f"❌ Erro em {dias_nome[d['dia_semana']]}: O horário de término deve ser posterior ao início.")
                                has_error = True

                            p_in = d["intervalo_inicio"]
                            p_fi = d["intervalo_fim"]
                            if p_in and p_fi:
                                if p_in >= p_fi:
                                    st.error(f"❌ Erro em {dias_nome[d['dia_semana']]}: O término da pausa deve ser posterior ao início.")
                                    has_error = True
                                if p_in < h_in or p_fi > h_fi:
                                    st.error(f"❌ Erro em {dias_nome[d['dia_semana']]}: A pausa deve estar contida dentro do horário de expediente.")
                                    has_error = True

                    if not has_error:
                        with st.spinner("Salvando disponibilidade..."):
                            suc, msg = availability_service.save_availability(user.get("id", 0), nova_grade, st.session_state.get("auth_token"))
                        if suc:
                            st.toast("Grade de horários salva com sucesso! 🎉")
                            st.success("✅ Sua grade de atendimento foi atualizada com sucesso.")
                        else:
                            st.error("❌ Não foi possível salvar a grade de atendimento.")

    # =========================================================================
    # VISÃO DO CLIENTE
    # =========================================================================
    else:
        nome_cliente = user.get('name', 'Cliente')
        data_formatada = ui_utils.format_date_long_pt_br()

        st.markdown(f"""
        <div style="margin-bottom:1.5rem;">
            <div style="font-size:2rem; font-weight:800; color:#F8FAFC; margin-bottom:0.25rem;">
                Olá, {nome_cliente}! 👋
            </div>
            <div style="font-size:0.95rem; color:#94A3B8; display:flex; align-items:center; gap:8px;">
                <span>📱 Área do Cliente</span>
                <span>•</span>
                <span>🗓️ {data_formatada}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        suc_c_apps, cliente_apps = appointment_service.get_appointments_by_user(user.get("id", 0), role="cliente", token=st.session_state.get("auth_token"))
        cliente_apps = cliente_apps or []
        apps_ativos = [a for a in cliente_apps if a.get("status") in ("confirmado", "pendente")]
        apps_passados = [a for a in cliente_apps if a.get("status") in ("concluido", "cancelado")]

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(ui_utils.metric_card_html("Agendamentos Ativos", str(len(apps_ativos)), "Próximos atendimentos", "📅"), unsafe_allow_html=True)
        with col_c2:
            st.markdown(ui_utils.metric_card_html("Total de Agendamentos", str(len(cliente_apps)), f"{len(apps_passados)} concluído(s) ou cancelado(s)", "🕒"), unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        tab_cli_catalogo, tab_cli_agendamentos = st.tabs(["🔍 Catálogo & Agendamento", "📅 Meus Agendamentos"])

        with tab_cli_catalogo:
            st.subheader("Catálogo de Serviços Disponíveis")
            st.markdown("Escolha um serviço abaixo, selecione a data e o horário desejado para agendar.")

            suc_pub, servicos_pub = catalog_service.get_public_services(token=st.session_state.get("auth_token"))
            if suc_pub and servicos_pub:
                cols = st.columns(2)
                for idx, serv in enumerate(servicos_pub):
                    with cols[idx % 2]:
                        with st.container(border=True):
                            st.markdown(f"#### ✂️ {serv.get('titulo')}")
                            if serv.get("descricao"):
                                st.write(serv.get("descricao"))
                            c_a, c_b = st.columns(2)
                            c_a.markdown(f"**💰 Valor:** {ui_utils.format_currency_brl(serv.get('preco', 0))}")
                            c_b.markdown(f"**⏱️ Duração:** {serv.get('duracao_minutos')} min")

                            with st.expander("📅 Selecionar Horário e Agendar", expanded=False):
                                s_id = serv.get("id")
                                p_id = serv.get("prestador_id", 15)
                                dur_min = serv.get("duracao_minutos", 30)

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
                                            st.toast("Agendamento confirmado com sucesso! 🎉")
                                            st.success(f"🎉 Agendamento confirmado para {ui_utils.format_date_short_pt_br(dt_escolhida)} às {slot_selecionado}!")
                                            st.rerun()
                                        else:
                                            st.error(f"❌ {resp_ag.get('message', 'Erro ao agendar.')}")
                                else:
                                    st.warning("Nenhum horário livre disponível para esta data.")
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "🔍",
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
                        col_a1.markdown(f"#### ✂️ {app.get('servico_titulo', 'Serviço')}")
                        data_cli_br = ui_utils.format_date_short_pt_br(app.get('data'))
                        col_a2.markdown(f"🗓️ **Data:** {data_cli_br} às **{app.get('hora_inicio')}**")
                        with col_a3:
                            st.markdown(ui_utils.status_badge_html(app.get("status")), unsafe_allow_html=True)

                        col_sub1, col_sub2, col_sub3 = st.columns([3, 2, 2])
                        col_sub1.caption(f"⏱️ Duração: {app.get('duracao_minutos')} min | Agendamento #{app.get('id')}")
                        col_sub2.markdown(f"💰 **{ui_utils.format_currency_brl(app.get('valor_cobrado', 0))}**")

                        with col_sub3:
                            st_app = app.get("status")
                            if st_app in ("confirmado", "pendente"):
                                if st.button("❌ Cancelar Agendamento", key=f"btn_cancel_cli_{app.get('id')}", use_container_width=True, type="secondary"):
                                    with st.spinner("Cancelando..."):
                                        appointment_service.update_appointment_status(app.get("id"), "cancelado", token=st.session_state.get("auth_token"))
                                    st.toast("Agendamento cancelado com sucesso!")
                                    st.rerun()
            else:
                st.markdown(
                    ui_utils.empty_state_html(
                        "📅",
                        "Você ainda não possui nenhum agendamento realizado",
                        "Acesse a aba 'Catálogo & Agendamento' para escolher um serviço e marcar seu primeiro atendimento."
                    ),
                    unsafe_allow_html=True
                )
