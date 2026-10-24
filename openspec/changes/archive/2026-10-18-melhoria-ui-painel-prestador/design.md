# Design Técnico: Melhoria da Interface do Painel do Prestador (AgendAí)

## Context
Ver `proposal.md` para motivação e justificativa. O frontend é implementado exclusivamente com Streamlit (`app.py`), consumindo a camada de serviços em `services/`. A tela do prestador necessita de reformulação visual para alcançar o padrão exigido na disciplina de Innovation Lab (UI moderna, ergonômica, tema escuro consistente, formatação pt-BR, legendas neutras e estados vazios amigáveis).

## Goals / Non-Goals

**Goals:**
- Configurar tema escuro sofisticado com suporte a alternância em `.streamlit/config.toml` (paleta harmoniosa: Slate/Obsidian, acentos em Azul/Indigo e Emerald).
- Exibir cabeçalho com saudação nominal correta baseada no usuário logado na sessão (`st.session_state["user"]`) e data atual por extenso em pt-BR.
- Redesenhar os cards de métricas (Agendamentos Hoje, Serviços Ativos, Preço Médio) eliminando deltas enganosos com setas verdes para cima em valores zerados.
- Formatar todos os valores numéricos monetários em Real brasileiro (`R$ XX,XX`) e datas no padrão `DD/MM/AAAA`.
- Implementar estados vazios amigáveis e acolhedores em todas as 4 abas (Resumo, Agenda, Meus Serviços, Grade de Atendimento).
- Enriquecer a barra lateral (Sidebar) com perfil completo do prestador (avatar/ícone, nome, email, badge de prestador e botão "Sair").
- Modularizar a renderização da UI em componentes/funções reutilizáveis e limpas.
- Otimizar carregamentos com `st.spinner`, toasts amigáveis e cache inteligente com `st.cache_data`.

**Non-Goals:**
- Não substituir Streamlit por React/Vue/Reflex (respeitar estritamente a decisão arquitetural).
- Não alterar contratos de endpoints de API nem tabelas no Xano.

## Decisions

### 1. Configuração de Tema Nativa em `.streamlit/config.toml`
- **Decisão**: Estabelecer as cores principais (primaryColor, backgroundColor, secondaryBackgroundColor, textColor, font) diretamente no arquivo de configuração do Streamlit, combinadas com CSS leve focado em microdetalhes estéticos (bordas, sombras suaves, badges).
- **Rationale**: Evita CSS excessivo ou frágil sujeito a quebras em atualizações de versão do Streamlit.

### 2. Resolução do Nome do Usuário
- **Decisão**: A saudação e identificação no painel consomem `user.get("name")` diretamente do `st.session_state["user"]`. O nome do prestador será padronizado como "Hector Barros" (alinhando com o email `hector.barros@aluno.impacta.edu.br`).

### 3. Métricas Customizadas Neutras
- **Decisão**: Usar cartões HTML estilizados ou `st.metric` sem o parâmetro `delta` positivo arbitrário. Quando o valor for zero ou neutro, utilizar texto explicativo simples e neutro (ex: "Sem atendimentos no dia").

### 4. Formatação e Utilitários
- **Decisão**: Criar funções utilitárias `format_currency_brl(value)` e `format_date_pt_br(dt)` para centralizar a apresentação de valores e datas em toda a interface.

## Risks / Trade-offs

- **[Risco de re-render excessivo no Streamlit]** → Mitigado pela persistência no `st.session_state` e separação das abas com renderização sob demanda.
- **[Risco de dados nulos nas métricas]** → Tratamento preventivo com valores padrão (`0.0`, listas vazias) garantindo robustez caso o banco esteja limpo.
