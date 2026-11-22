## Why

Na tela de Configurações da Conta (`render_account_settings_view`), estavam sendo exibidos simultaneamente dois botões de retorno ao painel:
1. Um botão no topo na barra de navegação principal ("⬅️ Voltar ao Painel").
2. Um botão no cabeçalho interno das configurações ("⬅️ Voltar").

Essa duplicidade gera redundância visual e poluição na interface. Conforme solicitado pelo usuário, **o botão superior duplicado deve ser removido** quando em modo de configurações, mantendo a interface limpa e elegante com um único botão claro de retorno ao painel.

## What Changes

- **Remoção do Botão Superior Duplicado em Configurações**:
  - Quando `view_mode == "settings"`, suprimir a renderização do botão duplicado na barra superior de `app.py`.
  - Manter apenas o botão de retorno dedicado e bem posicionado no cabeçalho das configurações (`btn_back_to_dashboard`), além do botão de Início na barra lateral fixa.
- **Harmonização do Topo da Página**:
  - Exibir apenas o breadcrumb informativo no topo ("📍 Você está em: Configurações da Conta") sem o botão redundante ao lado.

## Capabilities

### Modified Capabilities
- `prestador-dashboard`: Eliminar botão de retorno duplicado no topo da tela de configurações, garantindo uma navegação limpa com ponto único de ação.

## Impact

- **Código Afetado**: `app.py` (ajuste na condicional de renderização da barra de navegação superior).
- **APIs / Dados**: Nenhuma alteração.
