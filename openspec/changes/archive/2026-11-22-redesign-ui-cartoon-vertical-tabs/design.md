# Design: Visual Limpo com Abas Verticais, Ícones e Tipografia Cartoon

## 1. Arquitetura Visual e Tipografia

### 1.1 Tipografia Cartoon Amigável
A aplicação importará as fontes Google Fonts através da regra `@import` no topo de `clean_css` em `services/ui_utils.py`:
```css
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700;800&family=Quicksand:wght@500;600;700&display=swap');

html, body, [class*="st-"], .stApp, button, input, textarea, select, .stMarkdown {
    font-family: 'Fredoka', 'Quicksand', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Preserva fontes de ícones nativos do Streamlit/Material Icons para não quebrar ícones como 'expand_more' */
[class*="material-icons"],
[data-testid*="Icon"],
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
i[class*="icon"] {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
}
```
- **Fredoka**: Traz bordas e traços arredondados, visual lúdico e limpo, amplamente acessível e de alta legibilidade.
- **Títulos e Destaques**: `font-weight: 700` e `font-weight: 800`.
- **Preços, Status e Métricas**: Classes dedicadas ou seletores com `font-weight: 800 !important;` e cores contrastantes.
- **Proteção dos Ícones do Sistema**: O seletor universal não sobrescreve a fonte dos glyphs nativos de ícones do Streamlit (como o ícone de seta `expand_more` nos botões de popover e dropdowns).

### 1.2 Layout de Opções e Navegação na Vertical

Para garantir que a lista de abas/opções fique indiscutivelmente **na vertical** (uma opção abaixo da outra) sem conflitar com o empacotamento horizontal padrão do `st.tabs` do Streamlit:
1. **Navegação em Menu Vertical por Coluna Lateral**:
   - Criar divisão em duas colunas: coluna de opções vertical (esquerda, ex.: `st.columns([1, 3.5])`) e coluna de conteúdo da tela (direita).
   - Na coluna esquerda, renderizar os botões/itens em pilha vertical com ícones e destaque da opção selecionada.
   - Alternativamente, aplicar `div[data-testid="stTabs"] [data-baseweb="tab-list"] { flex-direction: column !important; }` com `display: block !important; width: 100% !important;` em cada botão de aba individual, eliminando o comportamento inline horizontal.
2. **Destaque Visual Estilo Cartoon**:
   - Item selecionado com fundo contrastante, borda arredondada (`border-radius: 14px`), tipografia em negrito (`font-weight: 800`) e ícone nítido.
   - Efeito hover suave para navegação tátil e intuitiva.

### 1.3 Ícones Contextuais das Abas
- **Prestador**:
  - `📊 Resumo`
  - `📅 Agenda de Atendimentos`
  - `✂️ Meus Serviços`
  - `⏰ Grade de Atendimento`
- **Cliente**:
  - `🤖 Assistente de Recomendação`
  - `📖 Catálogo Geral`
  - `🗓️ Meus Agendamentos`
- **Configurações**:
  - `👤 Perfil e Foto`
  - `🎨 Aparência (Tema)`
  - `🔒 Segurança e Senha`

### 1.4 Destaque em Negrito para Informações Críticas
- Preços: `ui_utils.format_currency_brl()` e tags de preço estilizadas com `font-weight: 800; font-size: 1.15rem;`.
- Status operacionais: Badges de status (Confirmado, Concluído, Pendente, Cancelado) com `font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;`.
- Métricas e avaliações: Valores de nota (ex: `★ 5.0`) e total de atendimentos/avaliações com `font-weight: 800;`.
