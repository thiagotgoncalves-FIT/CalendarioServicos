"""
AgendAí — Plataforma de Gestão e Agendamento para Prestadores Independentes
Frontend principal desenvolvido em Streamlit conectado ao backend Xano.
"""

import streamlit as st
from services import auth_service, api_client

st.set_page_config(
    page_title="AgendAí — Gestão e Agendamento",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Gerenciamento de Estado da Sessão (Session State)
# -----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None


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
        role_label = "✂️ Prestador de Serviços" if role == "prestador" else "📱 Cliente"

        st.markdown("---")
        st.markdown(f"**Usuário:** {user.get('name')}")
        st.markdown(f"**E-mail:** `{user.get('email')}`")
        st.markdown(f"**Perfil:** `{role_label}`")

        st.markdown("---")
        if st.button("🚪 Encerrar Sessão", use_container_width=True, type="secondary"):
            do_logout()
    else:
        st.info("🔒 Faça login ou crie uma conta para acessar a plataforma.")

    st.markdown("---")
    with st.expander("⚙️ Status da Conexão Xano"):
        api_url = api_client.API_BASE_URL
        is_placeholder = api_client.is_placeholder_url(api_url)
        if is_placeholder:
            st.warning("Ambiente em modo Local/Mock. Para conectar a API real do Xano, atualize a variável `XANO_API_URL` no `.env`.")
        else:
            st.success(f"Conectado ao Xano: `{api_url}`")


# -----------------------------------------------------------------------------
# Interface Principal: Não Autenticado (Login / Cadastro)
# -----------------------------------------------------------------------------
if not st.session_state["authenticated"]:
    st.title("Bem-vindo ao AgendAí 📅")
    st.markdown("""
    A plataforma web que elimina o atrito de agendamentos manuais pelo WhatsApp para prestadores autônomos
    (barbeiros, personal trainers, manicures, tutores) e seus clientes.
    """)

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
        with col_demo2:
            if st.button("📱 Entrar como Cliente (Mariana Silva)", use_container_width=True):
                success, response = auth_service.login("mariana@email.com", "123")
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["auth_token"] = response.get("authToken")
                    st.session_state["user"] = response.get("user")
                    st.rerun()

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
                pass_signup = st.text_input("Senha", type="password", placeholder="Mínimo 3 caracteres")

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

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Agendamentos Hoje", "0", delta="Pronto para novos agendamentos")
        with col2:
            st.metric("Serviços Ativos", "0", delta="Cadastrar serviços")
        with col3:
            st.metric("Receita Estimada", "R$ 0,00")

        st.markdown("---")
        st.subheader("📋 Suas Próximas Fatias no AgendAí")
        st.info("""
        ✅ **Fatia 1 Concluída**: Autenticação, perfis e retenção de sessão com Xano implementados!
        
        👉 **Próxima Fatia Recomendada (Fatia 2)**:
        - Cadastro e edição do Catálogo de Serviços (título, preço e duração em minutos).
        - Parametrização da Grade Semanal de Disponibilidade (dias e horários de trabalho).
        """)

    # Visão do Cliente
    else:
        st.title(f"Área do Cliente 📱")
        st.subheader(f"Olá, {user.get('name')}!")
        st.markdown("Encontre serviços dos seus profissionais favoritos e agende em poucos cliques.")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Seus Agendamentos", "0 ativos")
        with col2:
            st.metric("Histórico", "Nenhum agendamento realizado")

        st.markdown("---")
        st.subheader("🔍 Encontrar Profissionais")
        st.info("Assim que os prestadores cadastrarem seus serviços na próxima etapa, o catálogo completo estará disponível aqui para agendamento online!")
