# Tarefas: Redesign Visual com Abas Verticais, Ícones e Tipografia Cartoon

- [x] 1. Implementar injeção de fontes cartoon, proteção de ícones Material e CSS de abas verticais em `services/ui_utils.py` <!-- id: 1-inject-cartoon-font-and-vertical-tabs-css -->
  - Adicionar `@import` da família Google Fonts `Fredoka` e `Quicksand`.
  - Aplicar `font-family` cartoon universal para todo o aplicativo.
  - Adicionar regra de exceção e proteção para ícones nativos Material Symbols/Icons, prevenindo que o texto `expand_more` apareça por cima de botões como `st.popover`.
  - Implementar CSS flex para empilhamento vertical das abas com botões arredondados, padding confortável e destaques ativos.
  - Estilizar classes de dados críticos (preços, status, notas) com `font-weight: 800`.
  - Adaptar estilos para coerência total nos temas **Claro** e **Escuro**.

- [x] 2. Atualizar títulos de abas com ícones e garantir disposição vertical efetiva em `app.py` <!-- id: 2-update-tabs-labels-and-bold-weights -->
  - Configurar as opções em layout vertical real (coluna lateral de opções à esquerda com conteúdo à direita) nas áreas do Prestador, do Cliente e de Configurações.
  - Atualizar os rótulos de abas na Área do Prestador com ícones (`📊 Resumo`, `📅 Agenda de Atendimentos`, `✂️ Meus Serviços`, `⏰ Grade de Atendimento`).
  - Atualizar os rótulos de abas na Área do Cliente com ícones (`🤖 Assistente de Recomendação`, `📖 Catálogo Geral`, `🗓️ Meus Agendamentos`).
  - Atualizar os rótulos de abas em Configurações da Conta com ícones (`👤 Perfil e Foto`, `🎨 Aparência (Tema)`, `🔒 Segurança e Senha`).
  - Reforçar o negrito em preços, status e métricas nos cards e diálogos de serviço e agendamentos.

- [x] 3. Executar verificações de regressão e validação do OpenSpec <!-- id: 3-verify-and-validate -->
  - Executar as suítes de testes automatizados (`test_user_settings.py`, `test_review_system.py`, `test_appointment_engine.py`).
  - Validar a conformidade estrita da especificação com `openspec validate redesign-ui-cartoon-vertical-tabs --strict`.
