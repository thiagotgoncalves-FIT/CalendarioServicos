## Context

O projeto "AgendAí" é estruturado em Streamlit (Frontend) e Xano (Backend). O módulo de autenticação atual (`services/auth_service.py`) contém um banco de dados local mockado que mascara a ausência de comunicação com a API real do Xano, o que não reflete a realidade da arquitetura proposta. Ao mesmo tempo, o frontend público utiliza componentes nativos do Streamlit com design genérico.

## Goals / Non-Goals

**Goals:**
- Remover ou desativar completamente a lógica de "mock fallback" na autenticação, assegurando que o `signup` e `login` passem 100% pelos endpoints REST do Xano.
- Aplicar estilização com CSS customizado via `st.markdown(unsafe_allow_html=True)` focado na primeira tela (login e cadastro), com padrões estéticos modernos (cores e layouts que lembrem plataformas de SaaS).

**Non-Goals:**
- Modificar o fluxo de agendamentos ou dashboards internos nesta Change (somente a área deslogada/pública está no escopo).
- Migrar o frontend de Streamlit para outra tecnologia (Streamlit continua obrigatório).

## Decisions

**1. Estilização via Injeção de CSS**
- *Alternativas:* Usar bibliotecas externas como `streamlit-extras` ou injetar via `.streamlit/config.toml` e blocos `<style>`.
- *Decisão:* Faremos o setup primário das cores globais no `config.toml` para uniformidade de base, e então usaremos `st.markdown("<style>...</style>")` na página pública de login/signup para garantir alinhamentos e efeitos avançados.
- *Rationale:* É o método mais flexível que se adequa aos requerimentos de uma plataforma "profissional" em Streamlit sem quebrar a pilha padrão.

**2. Integração Xano como Single Source of Truth**
- *Alternativas:* Modificar os mocks para se comportarem com latência.
- *Decisão:* Os mocks na lista `_MOCK_USERS_DB` serão limpos ou bloqueados. Quando `data` do Xano retornar vazio ou erro, o `auth_service` levantará erro claro na interface do usuário (ex: "Falha de conexão" ou "Credenciais inválidas").
- *Rationale:* O objetivo é que o fluxo funcional de "criar um usuário e gravar no banco" aconteça no ambiente de produção real, garantindo a integridade dos dados que serão consumidos mais à frente (nas grades de horário).

## Risks / Trade-offs

- **Risco:** Alterações no DOM do Streamlit em novas versões da biblioteca podem quebrar o CSS customizado (pois dependem das classes `.stButton`, `.stApp`, etc.).
  - *Mitigação:* Usaremos as classes padrão documentadas que oferecem mais estabilidade.
- **Risco:** Ao remover os mocks, se o Xano não estiver respondendo ou a key `XANO_API_URL` não for configurada no `.env`, o App ficará bloqueado na tela de login.
  - *Mitigação:* Adicionar um tratamento de erro amigável na interface indicando explicitamente um problema de conexão.
