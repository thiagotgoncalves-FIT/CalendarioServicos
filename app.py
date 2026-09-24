import streamlit as st

st.set_page_config(
    page_title="Projeto Integrador - Innovation Lab",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Projeto Integrador")
st.subheader("Innovation Lab: Advanced No/Low Code")

st.success("✅ Ambiente Streamlit configurado com sucesso!")

with st.expander("ℹ️ Informações da Arquitetura e Ambiente", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎨 Frontend")
        st.write("**Streamlit** (Python)")
        st.caption("Tecnologia exclusiva para implementação da interface de usuário.")

    with col2:
        st.markdown("### ⚙️ Backend")
        st.write("**Xano** (No-Code / Low-Code)")
        st.caption("Banco de dados, autenticação, APIs REST e lógica serverless com XanoScript.")

    with col3:
        st.markdown("### 🤖 Engenharia de IA")
        st.write("**OpenSpec (SDD)**")
        st.caption("Desenvolvimento orientado a especificações e governança com Antigravity.")

st.info("💡 Próximo passo: Conectar os endpoints do Xano e especificar as mudanças incrementais no OpenSpec (`/opsx-propose`).")
