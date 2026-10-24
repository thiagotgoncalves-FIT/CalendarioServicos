# Proposta: Melhoria da Interface do Painel do Prestador

## Why
A interface atual do "Painel do Prestador" apresenta visual básico, hierarquia visual fraca, indicadores de métrica que passam sensação falsa de crescimento (setas verdes apontando para cima com valor zero), valores sem formatação brasileira (R$ 15.00 ao invés de R$ 15,00), ausência de estados vazios amigáveis e inconsistência na origem e grafia do nome do prestador logado. Esta melhoria eleva o padrão visual da plataforma AgendAí para um nível profissional, fluido e ergonômico, respeitando as diretrizes da disciplina e as restrições do Streamlit.

## What Changes
1. **Identidade Visual e Temas**: Configuração formal de tema consistente via `.streamlit/config.toml` (dark mode elegante com suporte a light mode) e eliminação de CSS frágil/excessivo.
2. **Cabeçalho e Contexto do Usuário**: Boas-vindas personalizadas consumindo diretamente os dados do usuário autenticado na sessão (`st.session_state["user"]`), data de hoje em português (ex: "18 de outubro de 2026") e identificação clara do negócio/perfil.
3. **Aba Resumo**:
   - Cartões de métricas com ícone temático, valor em destaque e legendas neutras/informativas (sem setas enganosas de delta quando o valor for zero).
   - Formatação consistente em pt-BR para moeda (`R$ XX,XX`), datas e horários.
   - Lista/tabela de atendimentos do dia com estado vazio amigável ("Você ainda não tem agendamentos hoje").
4. **Aba Agenda de Atendimentos**: Filtros refinados por data e status com tags visuais coloridas (Pendente, Confirmado, Concluído, Cancelado) e botões de ação rápida com feedback claro.
5. **Aba Meus Serviços**: Gestão de catálogo com visual em cartões com nome, duração, preço formatado em BRL, badge de status ativo/inativo e formulário modal/expansível com validação e mensagens claras.
6. **Aba Grade de Atendimento**: Configuração visual e intuitiva da jornada semanal, validações de horário (início < fim, pausa contida no expediente) e feedback imediato de gravação.
7. **Barra Lateral (Sidebar)**: Perfil do usuário com avatar/ícone, badge do perfil `prestador`, navegação limpa e botão de logout ("Sair").
8. **Feedback e Desempenho**: `st.spinner` durante chamadas, `st.toast`/`st.success`/`st.error` sem vazamento de stack traces técnicos, cache com TTL via `st.cache_data` com invalidação em operações de escrita (mutations).

## Capabilities

### New Capabilities
- `prestador-dashboard`: Métricas resumidas do prestador, formatação pt-BR, cabeçalho contextual e estados vazios amigáveis.

### Modified Capabilities
- `service-catalog`: Interface amigável de catálogo de serviços com validação no formulário e visualização refinada.
- `prestador-availability`: Interface intuitiva de grade semanal de horários com validações interativas.
- `appointment-engine`: Visualização de agendamentos com filtros dinâmicos e ações rápidas no painel do prestador.

## Impact
- **Frontend (`app.py`, `.streamlit/config.toml`)**: Reestruturação modular da tela do prestador em componentes visuais limpos e organizados.
- **Camada de Serviços (`services/`)**: Centralização das chamadas, formatação utilitária brasileira e invalidação de cache controlada.
- **Contratos de API**: Nenhum endpoint terá contrato alterado; total retrocompatibilidade mantida.
