"""
AgendAí — Plataforma de Gestão e Agendamento para Prestadores Independentes
Frontend principal desenvolvido em Streamlit conectado ao backend Xano.
"""

import streamlit as st
from datetime import date, datetime, time
from services import auth_service, api_client, catalog_service, availability_service, appointment_service

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
        padding: 2.2rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Inputs Escuros e Estilizados */
    .stTextInput input, .stNumberInput input {
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

    /* Badges de Perfil */
    .profile-card {
        background: #111827;
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 1rem 0;
    }
    .badge-prestador {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-cliente {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Limpeza geral */
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
    """Limpa os dados de autenticação e encerra a sessão."""
    st.session_state["authenticated"] = False
    st.session_state["auth_token"] = None
    st.session_state["user"] = None
    st.rerun()


# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("📅 AgendAí")
    st.caption("Innovation Lab: Advanced No/Low Code — Impacta")

    if st.session_state["authenticated"]:
        user = st.session_state["user"]
        role = user.get("role", "cliente")
        badge_class = "badge-prestador" if role == "prestador" else "badge-cliente"
        role_label = "✂️ Prestador de Serviços" if role == "prestador" else "📱 Cliente"

        st.markdown(f"""
        <div class="profile-card">
            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 4px;">Sessão Ativa</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 2px;">{user.get('name')}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 8px;">{user.get('email')}</div>
            <span class="{badge_class}">{role_label}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Encerrar Sessão", use_container_width=True, type="secondary"):
            do_logout()
    else:
        st.info("🔒 Faça login ou crie uma conta para acessar a plataforma.")

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
    st.markdown('<div class="hero-subtitle">A plataforma de gestão e agendamento que elimina atritos de agendamento manual no WhatsApp para prestadores autônomos e seus clientes.</div>', unsafe_allow_html=True)

    tab_login, tab_signup, tab_about = st.tabs(["🔑 Entrar", "📝 Criar Conta", "ℹ️ Sobre o Projeto"])

    # Aba: Login
    with tab_login:
        st.subheader("Acesse sua conta")
        with st.form("form_login"):
            email_login = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
            pass_login = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submit_login = st.form_submit_button("Entrar no AgendAí", use_container_width=True, type="primary")

            if submit_login:
                success, response = auth_service.login(email_login, pass_login)
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["auth_token"] = response.get("authToken")
                    st.session_state["user"] = response.get("user")
                    st.success("✅ Login realizado com sucesso! Redirecionando...")
                    st.rerun()
                else:
                    st.error(f"❌ {response.get('message', 'Erro ao efetuar login.')}")
        
        if not st.session_state.get("show_recovery"):
            if st.button("🔐 Esqueceu sua senha? Clique aqui para recuperar", use_container_width=True):
                st.session_state["show_recovery"] = True
                st.rerun()
        else:
            st.markdown("---")
            st.info("Preencha seu e-mail abaixo para receber as instruções de recuperação de senha.")
            with st.form("form_recovery"):
                email_recovery = st.text_input("E-mail cadastrado", placeholder="seu.email@exemplo.com")
                submit_recovery = st.form_submit_button("Enviar instruções de recuperação", use_container_width=True, type="primary")
                if submit_recovery:
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
            if st.button("✂️ Entrar como Prestador (Carlos Barbeiro)", use_container_width=True):
                success, response = auth_service.login("carlos@barbearia.com", "123")
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["auth_token"] = response.get("authToken")
                    st.session_state["user"] = response.get("user")
                    st.rerun()
                else:
                    st.error(f"❌ {response.get('message', 'Erro no acesso de demonstração.')}")
        with col_demo2:
            if st.button("📱 Entrar como Cliente (Mariana Silva)", use_container_width=True):
                success, response = auth_service.login("mariana@email.com", "123")
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["auth_token"] = response.get("authToken")
                    st.session_state["user"] = response.get("user")
                    st.rerun()
                else:
                    st.error(f"❌ {response.get('message', 'Erro no acesso de demonstração.')}")

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
                pass_signup = st.text_input("Senha", type="password", placeholder="Mínimo 8 caracteres (Maiúscula, minúscula, número e símbolo)")

            role_choice = st.radio(
                "Qual é o seu perfil de uso?",
                options=["prestador", "cliente"],
                format_func=lambda r: "✂️ Prestador de Serviços (quero divulgar horários e gerenciar clientes)" if r == "prestador" else "📱 Cliente (quero agendar serviços com facilidade)",
                horizontal=False
            )

            submit_signup = st.form_submit_button("Cadastrar e Começar", use_container_width=True, type="primary")

            if submit_signup:
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
                    st.success("🎉 Conta criada com sucesso! Entrando na plataforma...")
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

    # Visão do Prestador de Serviços
    if role == "prestador":
        st.title(f"Painel do Prestador ✂️")
        st.subheader(f"Olá, {user.get('name')}!")
        st.markdown("Aqui você gerencia seus serviços, sua grade de horários e os agendamentos dos clientes.")

        tab_resumo, tab_agenda, tab_catalogo, tab_grade = st.tabs([
            "📊 Resumo", "📅 Agenda de Atendimentos", "✂️ Meus Serviços", "🕒 Grade de Atendimento"
        ])

        with tab_resumo:
            sucesso_cat, servicos = catalog_service.get_services(user.get("id", 0), st.session_state.get("auth_token"))
            ativos = [s for s in servicos if s.get("ativo")] if sucesso_cat else []
            qtd_ativos = len(ativos)
            preco_medio = sum(float(s["preco"]) for s in ativos) / qtd_ativos if qtd_ativos > 0 else 0.0

            _, prestador_apps = appointment_service.get_appointments_by_user(user.get("id", 0), role="prestador", token=st.session_state.get("auth_token"))
            today_str = date.today().strftime("%Y-%m-%d")
            apps_hoje = [a for a in prestador_apps if a.get("data") == today_str and a.get("status") in ("confirmado", "pendente", "concluido")]
            receita_prevista = sum(float(a.get("valor_cobrado", 0)) for a in prestador_apps if a.get("status") in ("confirmado", "concluido"))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Agendamentos Hoje", str(len(apps_hoje)), delta=f"{len(apps_hoje)} para hoje")
            with col2:
                st.metric("Serviços Ativos", str(qtd_ativos), delta="Em seu catálogo")
            with col3:
                st.metric("Preço Médio", f"R$ {preco_medio:.2f}", delta=f"R$ {receita_prevista:.2f} previstos")

        with tab_agenda:
            st.subheader("📅 Gestão de Atendimentos e Horários")
            st.markdown("Consulte e gerencie o ciclo de vida das reservas feitas pelos seus clientes.")

            suc_apps_agenda, todos_apps = appointment_service.get_appointments_by_user(user.get("id", 0), role="prestador", token=st.session_state.get("auth_token"))

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filtro_status = st.selectbox(
                    "Filtrar por Status",
                    options=["Todos", "confirmado", "pendente", "concluido", "cancelado"],
                    key="prestador_filtro_status"
                )
            with col_f2:
                filtro_data = st.date_input(
                    "Filtrar por Data (Deixe em branco para ver todas)",
                    value=None,
                    key="prestador_filtro_data"
                )

            apps_filtrados = todos_apps or []
            if filtro_status != "Todos":
                apps_filtrados = [a for a in apps_filtrados if a.get("status") == filtro_status]
            if filtro_data:
                data_str_f = filtro_data.strftime("%Y-%m-%d")
                apps_filtrados = [a for a in apps_filtrados if a.get("data") == data_str_f]

            if apps_filtrados:
                for a in apps_filtrados:
                    with st.container(border=True):
                        c_h1, c_h2, c_h3 = st.columns([3, 2, 2])
                        c_h1.markdown(f"#### ✂️ {a.get('servico_titulo', 'Serviço')}")
                        c_h2.markdown(f"🗓️ **Data:** {a.get('data')} às **{a.get('hora_inicio')}**")
                        
                        st_val = a.get("status")
                        if st_val == "confirmado":
                            c_h3.success("Confirmado")
                        elif st_val == "concluido":
                            c_h3.info("Concluído")
                        elif st_val == "pendente":
                            c_h3.warning("Pendente")
                        else:
                            c_h3.error("Cancelado")

                        c_det1, c_det2, c_det3 = st.columns([3, 2, 2])
                        c_det1.caption(f"👤 Cliente #{a.get('cliente_id')} | ⏱️ Duração: {a.get('duracao_minutos')} min")
                        c_det2.markdown(f"💰 **R$ {float(a.get('valor_cobrado', 0)):.2f}**")

                        with c_det3:
                            if st_val in ("confirmado", "pendente"):
                                col_b1, col_b2 = st.columns(2)
                                with col_b1:
                                    if st.button("✅ Concluir", key=f"btn_concluir_{a.get('id')}", use_container_width=True):
                                        appointment_service.update_appointment_status(a.get("id"), "concluido", token=st.session_state.get("auth_token"))
                                        st.success("Atendimento marcado como concluído!")
                                        st.rerun()
                                with col_b2:
                                    if st.button("❌ Cancelar", key=f"btn_cancel_prest_{a.get('id')}", use_container_width=True, type="secondary"):
                                        appointment_service.update_appointment_status(a.get("id"), "cancelado", token=st.session_state.get("auth_token"))
                                        st.warning("Agendamento cancelado.")
                                        st.rerun()
            else:
                st.info("Nenhum agendamento encontrado para os filtros selecionados.")

        with tab_catalogo:
            st.subheader("Catálogo de Serviços")
            
            with st.expander("➕ Adicionar Novo Serviço", expanded=False):
                with st.form("form_new_service"):
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        titulo = st.text_input("Título do Serviço", placeholder="Ex: Corte Degradê")
                        preco = st.number_input("Preço (R$)", min_value=0.0, step=5.0)
                    with col_s2:
                        duracao = st.number_input("Duração (minutos)", min_value=15, step=15)
                        descricao = st.text_input("Breve descrição (Opcional)")
                    
                    submit_service = st.form_submit_button("Salvar Serviço", type="primary")
                    if submit_service:
                        if not titulo:
                            st.error("O título é obrigatório!")
                        else:
                            suc, msg = catalog_service.create_service(
                                prestador_id=user.get("id", 0),
                                titulo=titulo,
                                preco=preco,
                                duracao_minutos=duracao,
                                descricao=descricao,
                                token=st.session_state.get("auth_token")
                            )
                            if suc:
                                st.success("Serviço adicionado com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao adicionar serviço.")

            st.markdown("### Seus serviços cadastrados")
            if sucesso_cat and servicos:
                for s in servicos:
                    with st.container():
                        st.markdown(f"**{s['titulo']}**")
                        if s.get('descricao'):
                            st.caption(f"{s['descricao']}")
                        
                        col_i1, col_i2, col_i3, col_i4 = st.columns([2,2,2,3])
                        col_i1.markdown(f"💰 R$ {float(s['preco']):.2f}")
                        col_i2.markdown(f"⏱️ {s['duracao_minutos']} min")
                        if s.get('ativo'):
                            col_i3.success("Ativo")
                            if col_i4.button("Desativar", key=f"desativar_{s['id']}", type="secondary"):
                                catalog_service.toggle_service_status(s["id"], False, st.session_state.get("auth_token"))
                                st.rerun()
                        else:
                            col_i3.error("Inativo")
                            if col_i4.button("Reativar", key=f"reativar_{s['id']}", type="secondary"):
                                catalog_service.toggle_service_status(s["id"], True, st.session_state.get("auth_token"))
                                st.rerun()
                        st.divider()
            else:
                st.info("Nenhum serviço cadastrado ainda.")

        with tab_grade:
            st.subheader("Configuração da Grade de Atendimento")
            st.markdown("Defina os dias da semana e os horários em que você atende.")
            
            suc_grade, grade_atual = availability_service.get_availability(user.get("id", 0), st.session_state.get("auth_token"))
            if not grade_atual:
                # Grade padrão caso não exista
                grade_atual = [
                    {"dia_semana": i, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": (1 <= i <= 5)} 
                    for i in range(7)
                ]
            
            dias_nome = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
            
            nova_grade = []
            
            with st.form("form_grade_atendimento"):
                from datetime import time
                def str_to_time(t_str):
                    if not t_str: return None
                    try:
                        h, m = map(int, t_str.split(':')[:2])
                        return time(h, m)
                    except:
                        return None

                for dia_idx in range(7):
                    # Encontrar os dados do dia específico
                    dados_dia = next((d for d in grade_atual if d["dia_semana"] == dia_idx), None)
                    if not dados_dia:
                        dados_dia = {"dia_semana": dia_idx, "hora_inicio": "09:00", "hora_fim": "18:00", "intervalo_inicio": "12:00", "intervalo_fim": "13:00", "ativo": False}
                    
                    st.markdown(f"**{dias_nome[dia_idx]}**")
                    col_ativo, col_ini, col_fim, col_int_ini, col_int_fim = st.columns(5)
                    
                    ativo = col_ativo.checkbox("Atender neste dia", value=dados_dia.get("ativo", False), key=f"ativo_{dia_idx}")
                    
                    h_ini = str_to_time(dados_dia.get("hora_inicio")) or time(9, 0)
                    h_fim = str_to_time(dados_dia.get("hora_fim")) or time(18, 0)
                    
                    # Pausa (pode ser nulo)
                    int_ini = str_to_time(dados_dia.get("intervalo_inicio")) or time(12, 0)
                    int_fim = str_to_time(dados_dia.get("intervalo_fim")) or time(13, 0)
                    # Caso o backend tenha retornado None para pausa, usaremos esse controle visual
                    has_pausa = col_ativo.checkbox("Tem pausa?", value=bool(dados_dia.get("intervalo_inicio")), key=f"tem_pausa_{dia_idx}", disabled=not ativo)
                    
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
                    st.divider()
                
                submit_grade = st.form_submit_button("Salvar Grade de Atendimento", type="primary", use_container_width=True)
                
                if submit_grade:
                    has_error = False
                    for d in nova_grade:
                        if d["ativo"]:
                            h_in = d["hora_inicio"]
                            h_fi = d["hora_fim"]
                            if h_in and h_fi and h_in >= h_fi:
                                st.error(f"❌ Erro em {dias_nome[d['dia_semana']]}: O horário de término deve ser depois do início.")
                                has_error = True
                            
                            p_in = d["intervalo_inicio"]
                            p_fi = d["intervalo_fim"]
                            if p_in and p_fi:
                                if p_in >= p_fi:
                                    st.error(f"❌ Erro em {dias_nome[d['dia_semana']]}: O fim da pausa deve ser depois do início.")
                                    has_error = True
                                if p_in < h_in or p_fi > h_fi:
                                    st.error(f"❌ Erro em {dias_nome[d['dia_semana']]}: A pausa deve estar totalmente contida dentro do horário de expediente.")
                                    has_error = True

                    if not has_error:
                        suc, msg = availability_service.save_availability(user.get("id", 0), nova_grade, st.session_state.get("auth_token"))
                        if suc:
                            st.success("✅ Grade de horários salva com sucesso!")
                        else:
                            st.error("❌ Erro ao salvar a grade.")

    # Visão do Cliente
    else:
        st.title(f"Área do Cliente 📱")
        st.subheader(f"Olá, {user.get('name')}!")
        st.markdown("Encontre serviços dos seus profissionais favoritos e agende em poucos cliques.")

        suc_c_apps, cliente_apps = appointment_service.get_appointments_by_user(user.get("id", 0), role="cliente", token=st.session_state.get("auth_token"))
        apps_ativos = [a for a in cliente_apps if a.get("status") in ("confirmado", "pendente")]
        apps_passados = [a for a in cliente_apps if a.get("status") in ("concluido", "cancelado")]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Agendamentos Ativos", f"{len(apps_ativos)} ativo(s)", delta="Próximos atendimentos")
        with col2:
            st.metric("Histórico de Agendamentos", f"{len(cliente_apps)} no total", delta=f"{len(apps_passados)} concluídos/cancelados")

        st.markdown("---")
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
                            c_a.markdown(f"**💰 Valor:** R$ {float(serv.get('preco', 0)):.2f}")
                            c_b.markdown(f"**⏱️ Duração:** {serv.get('duracao_minutos')} min")

                            with st.expander(f"📅 Selecionar Horário e Agendar", expanded=False):
                                s_id = serv.get("id")
                                p_id = serv.get("prestador_id", 1)
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
                                        suc_ag, resp_ag = appointment_service.create_appointment(
                                            cliente_id=user.get("id", 0),
                                            prestador_id=p_id,
                                            servico_id=s_id,
                                            data_str=dt_escolhida_str,
                                            hora_inicio=slot_selecionado,
                                            token=st.session_state.get("auth_token")
                                        )
                                        if suc_ag:
                                            st.success(f"🎉 Agendamento confirmado para {dt_escolhida.strftime('%d/%m/%Y')} às {slot_selecionado}!")
                                            st.rerun()
                                        else:
                                            st.error(f"❌ {resp_ag.get('message', 'Erro ao agendar.')}")
                                else:
                                    st.warning("Nenhum horário livre disponível para esta data.")
            else:
                st.info("Nenhum serviço ativo disponível no momento.")

        with tab_cli_agendamentos:
            st.subheader("Seus Agendamentos Realizados")
            st.markdown("Consulte seus atendimentos programados e histórico de agendamentos.")

            if cliente_apps:
                for app in cliente_apps:
                    with st.container(border=True):
                        col_a1, col_a2, col_a3 = st.columns([3, 2, 2])
                        col_a1.markdown(f"#### ✂️ {app.get('servico_titulo', 'Serviço')}")
                        col_a2.markdown(f"🗓️ **Data:** {app.get('data')} às **{app.get('hora_inicio')}**")

                        st_app = app.get("status")
                        if st_app == "confirmado":
                            col_a3.success("Confirmado")
                        elif st_app == "concluido":
                            col_a3.info("Concluído")
                        elif st_app == "pendente":
                            col_a3.warning("Pendente")
                        else:
                            col_a3.error("Cancelado")

                        col_sub1, col_sub2, col_sub3 = st.columns([3, 2, 2])
                        col_sub1.caption(f"⏱️ Duração: {app.get('duracao_minutos')} min | Agendamento #{app.get('id')}")
                        col_sub2.markdown(f"💰 **R$ {float(app.get('valor_cobrado', 0)):.2f}**")

                        with col_sub3:
                            if st_app in ("confirmado", "pendente"):
                                if st.button("❌ Cancelar Agendamento", key=f"btn_cancel_cli_{app.get('id')}", use_container_width=True, type="secondary"):
                                    appointment_service.update_appointment_status(app.get("id"), "cancelado", token=st.session_state.get("auth_token"))
                                    st.warning("Agendamento cancelado com sucesso!")
                                    st.rerun()
            else:
                st.info("Você ainda não possui nenhum agendamento realizado.")
