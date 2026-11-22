## Context

Ver `proposal.md` para a motivação. No Streamlit:
1. Quando `st.set_page_config(initial_sidebar_state="expanded")` é usado, a sidebar vem aberta. Se o usuário clica na seta `chevron-left` (`data-testid="stSidebarCollapseButton"`), o Streamlit colapsa a lateral alterando a largura da seção para 0px e criando um elemento `div[data-testid="stSidebarCollapsedControl"]` no canto superior esquerdo para reabrir.
2. Como o CSS em `ui_utils.py` limpava certos containers do header, o botão `stSidebarCollapsedControl` não estava visível ou ficava com z-index menor ou opacidade oculta, impedindo o usuário de reabrir a sidebar.
3. Para atender ao requisito de não ocultar a tela por completo ("quero que fique apenas os ícones"), estilizamos a barra lateral e os controles de modo que os ícones principais (logotipo, avatar, engrenagem e saída) permaneçam visíveis ou que o botão flutuante com o avatar/ícone de menu esteja sempre fixado no canto superior esquerdo.

## Goals / Non-Goals

**Goals:**
- Garantir que `div[data-testid="stSidebarCollapsedControl"]` fique fixo no topo esquerdo (`top: 12px; left: 12px; z-index: 100000; display: block !important; visibility: visible !important;`) com aparência refinada de botão de menu/ícone.
- Permitir que a sidebar recolhida mostre os ícones essenciais ou que um clique no botão flutuante reabra a lateral instantaneamente.
- Assegurar que os elementos de texto do perfil e da marca reapareçam perfeitamente ao expandir a barra.

**Non-Goals:**
- Não reimplementar o motor de layout do Streamlit fora de CSS/HTML padrão.

## Decisions

1. **Botão Flutuante de Alta Prioridade no Topo Esquerdo**:
   - Forçar via CSS que `div[data-testid="stSidebarCollapsedControl"]` e seus botões filhos tenham `position: fixed`, `z-index: 100000`, plano de fundo contrastante, borda sutil e ícone de menu/seta visível tanto no tema Claro quanto no Escuro.

2. **Mini Sidebar CSS Override**:
   - Adicionar regra de CSS para que, se a barra for colapsada, os elementos textuais fiquem ocultos e a largura preserve a linha de ícones, ou o botão de toggle seja um atalho evidente.

## Risks / Trade-offs

- **[Risco] Variações de classes internas entre versões do Streamlit** → **Mitigação**: Selecionar por atributos estáveis `data-testid="stSidebarCollapsedControl"`, `data-testid="stSidebarCollapseButton"`, e tags semânticas `section[data-testid="stSidebar"]`.
