## 1. Ajuste de CSS e Controle de Colapso da Barra Lateral

- [x] 1.1 Configurar em `services/ui_utils.py` a exibição fixa e de alto contraste para `div[data-testid="stSidebarCollapsedControl"]` e `button[data-testid="stSidebarCollapseButton"]`, garantindo que o botão de reabertura da barra lateral esteja sempre visível e interativo no canto superior esquerdo.
- [x] 1.2 Implementar estilo visual de mini barra lateral (recolhimento com foco em ícones e transição fluida) tanto para o Tema Claro quanto para o Tema Escuro.

## 2. Testes e Validação

- [x] 2.1 Executar a suíte de testes automatizados do projeto garantindo integridade de estilos e funcionalidades.
- [x] 2.2 Validar a change no OpenSpec com `openspec validate fix-sidebar-collapse-e-restauracao --strict`.
