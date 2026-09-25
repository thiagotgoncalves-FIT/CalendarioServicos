import streamlit as st

st.set_page_config(
    page_title="AgendAí — Gestão e Agendamento Online",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📅 AgendAí")
st.subheader("Plataforma de Gestão e Agendamento para Prestadores Independentes")
st.caption("Innovation Lab: Advanced No/Low Code — Faculdade IMPACTA (Prof. Leonardo Bontempo)")

st.success("✅ Ambiente AgendAí configurado com sucesso! Pronto para integração com o Xano.")

st.markdown("""
### 💡 Sobre a Plataforma
O **AgendAí** elimina o atrito de agendamentos manuais pelo WhatsApp para profissionais autônomos
(barbeiros, personal trainers, manicures, tutores, etc.), acabando com conflitos de agenda e furos de clientes.
""")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### ✂️ Para o Prestador de Serviços")
    st.write("- Cadastro de catálogo de serviços (título, preço e duração).")
    st.write("- Parametrização da grade de horários disponíveis e pausas.")
    st.write("- Gestão de agenda diária e controle de status dos agendamentos.")

with col_right:
    st.markdown("#### 📱 Para o Cliente")
    st.write("- Visualização rápida do catálogo de serviços do profissional.")
    st.write("- Seleção inteligente de datas e horários livres em tempo real.")
    st.write("- Confirmação ágil do agendamento em poucos cliques.")

with st.expander("ℹ️ Arquitetura e Engenharia do Projeto", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎨 Frontend")
        st.write("**Streamlit** (Python 3.14)")
        st.caption("Interface web interativa e ágil para prestadores e clientes.")

    with col2:
        st.markdown("### ⚙️ Backend")
        st.write("**Xano** (No-Code / Low-Code)")
        st.caption("Modelagem relacional, regras de negócio anti-conflito e APIs REST seguras.")

    with col3:
        st.markdown("### 🤖 Metodologia")
        st.write("**OpenSpec (SDD)**")
        st.caption("Desenvolvimento guiado por especificações no ambiente Antigravity.")

st.info("💡 Próximo passo recomendado: Iniciar a primeira especificação funcional via `/opsx-propose` (ex.: autenticação ou catálogo de serviços).")
