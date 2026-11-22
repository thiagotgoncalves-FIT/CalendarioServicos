## Context

O usuário relatou: *"na parte de configurações existem dois botões de voltar, retire o botão de voltar que esta em cima"* e enviou uma imagem mostrando os dois botões: o "⬅️ Voltar ao Painel" (na barra superior externa) e o "⬅️ Voltar" (no cabeçalho da visualização de configurações).

## Goals / Non-Goals

**Goals:**
- Remover o botão superior "⬅️ Voltar ao Painel" da barra de navegação no topo quando o usuário estiver na tela de configurações.
- Preservar apenas o botão de retorno oficial no cabeçalho da seção de configurações ("⬅️ Voltar").
- Manter o botão "⚙️ Configurações" disponível quando o usuário estiver no painel principal ("dashboard").

**Non-Goals:**
- Não alterar as abas internas nem os formulários de configurações.

## Decisions

1. **Condicional na Barra de Navegação Superior (`app.py`)**:
   - Se `view_mode == "settings"`: a coluna de ações da barra superior não renderiza o botão "Voltar ao Painel" (ou exibe apenas o breadcrumb informativo).
   - Se `view_mode == "dashboard"`: continua exibindo o atalho para "⚙️ Configurações".
2. **Ponto Único de Retorno**:
   - O cabeçalho de `render_account_settings_view` concentra o botão principal "⬅️ Voltar" para retornar a `view_mode = "dashboard"`.
