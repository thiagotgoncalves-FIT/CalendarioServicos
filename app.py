"""
AgendAí — Plataforma de Gestão e Agendamento para Prestadores Independentes
Frontend principal desenvolvido em Streamlit conectado ao backend Xano.
"""

import streamlit as st
from services import auth_service, api_client, catalog_service, availability_service

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

        tab_resumo, tab_catalogo, tab_grade = st.tabs(["📊 Resumo", "✂️ Meus Serviços", "🕒 Grade de Atendimento"])

        with tab_resumo:
            sucesso_cat, servicos = catalog_service.get_services(user["id"], st.session_state.get("auth_token"))
            ativos = [s for s in servicos if s.get("ativo")] if sucesso_cat else []
            qtd_ativos = len(ativos)
            preco_medio = sum(float(s["preco"]) for s in ativos) / qtd_ativos if qtd_ativos > 0 else 0.0

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Agendamentos Hoje", "0", delta="Pronto para novos agendamentos")
            with col2:
                st.metric("Serviços Ativos", str(qtd_ativos), delta="Em seu catálogo")
            with col3:
                st.metric("Preço Médio", f"R$ {preco_medio:.2f}")

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
                                prestador_id=user["id"],
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
            
            suc_grade, grade_atual = availability_service.get_availability(user["id"], st.session_state.get("auth_token"))
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
                        suc, msg = availability_service.save_availability(user["id"], nova_grade, st.session_state.get("auth_token"))
                        if suc:
                            st.success("✅ Grade de horários salva com sucesso!")
                        else:
                            st.error("❌ Erro ao salvar a grade.")

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
