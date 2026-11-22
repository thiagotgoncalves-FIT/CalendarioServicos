## Why

Ao recolher a barra lateral no Streamlit (clicando no botão de seta de colapso), todo o painel lateral é fechado e ocultado da tela. O botão nativo para reexpandir a barra lateral (`div[data-testid="stSidebarCollapsedControl"]`) não estava aparecendo para o usuário reabri-la. Além disso, o usuário deseja que, ao recolher a lateral, a área do menu não suma por completo: ela deve se transformar em uma coluna estreita (mini barra lateral de ícones) preservando o logotipo, o avatar e os botões de ação rápida (Configurações e Sair), permitindo expandir e recolher facilmente.

## What Changes

- **Restauração e Visibilidade Confiável da Barra Lateral**:
  - Garantir que a barra lateral permaneça sempre acessível e que o botão de controle de expansão/reabertura (`stSidebarCollapsedControl`) esteja posicionado e visível no topo esquerdo da viewport caso a barra seja fechada.
- **Modo Mini Barra Lateral com Ícones**:
  - Implementar suporte via CSS/layout para exibir uma barra lateral compacta (mini-sidebar com ~60-70px de largura quando recolhida ou botão flutuante persistente), exibindo apenas os ícones (Logotipo 'A', Avatar circular do usuário, ícone ⚙️ de configurações e ícone 🚪/Sair).
  - Garantir que os dados do usuário logado (nome, e-mail e badge) continuem renderizando normalmente no modo expandido.

## Capabilities

### Modified Capabilities
- `prestador-dashboard`: Garantir que os controles de navegação e identificação do usuário logado na barra lateral permaneçam visíveis e acessíveis tanto no modo expandido quanto no modo recolhido (mini-sidebar de ícones).

## Impact

- **Código Afetado**: `services/ui_utils.py` (regras de CSS de `apply_theme_and_clean_ui` e visibilidade do controle de colapso), `app.py` (estrutura e classes da barra lateral).
- **APIs / Dados**: Nenhuma alteração em chamadas de API ou banco de dados.
