## Purpose

Estabelece o design system, a identidade visual moderna e os componentes padronizados de interface para toda a plataforma AgendAí em Streamlit.

## ADDED Requirements

### Requirement: Design System e Identidade Visual Coesa
O sistema MUST aplicar em 100% das telas da aplicação (autenticação, painel do cliente, catálogo, assistente, painel do prestador e agenda) um design system moderno, profissional e limpo, baseado em paleta de cores consistente (tons escuros refinados com destaque azul/esmeralda), tipografia legível, espaçamentos uniformes e hierarquia visual clara, eliminando excessos decorativos e bordas pesadas.

#### Scenario: Consistência Visual entre Portais de Cliente e Prestador
- **WHEN** o usuário transita entre diferentes visões ou páginas do sistema
- **THEN** a interface mantém padronização de fontes, espaçamentos, estilos de botões e cartões sem quebra de identidade visual

### Requirement: Componentes Reutilizáveis de Cards, Formulários e Feedbacks
O sistema MUST utilizar componentes padronizados e reutilizáveis para exibição de serviços, perfis de profissionais, métricas de resumo, formulários validados e notificações de feedback (toasts, spinners de carregamento e estados vazios amigáveis).

#### Scenario: Apresentação Padronizada de Cards de Serviços
- **WHEN** serviços são listados no catálogo, na recomendação ou no painel de gestão
- **THEN** os cards apresentam estrutura consistente com título legível, preço formatado em BRL (`R$ XX,XX`), duração estimada e ações claras

#### Scenario: Feedback Visual Não-Bloqueante
- **WHEN** uma operação de consulta, atualização ou agendamento é disparada
- **THEN** o sistema exibe indicadores visuais sutis de processamento e confirmações via toasts estilizados sem poluição visual

### Requirement: Navegação Intuitiva e Acessível
O sistema MUST estruturar a navegação de forma direta e previsível, permitindo que as ações primárias (buscar, agendar, gerenciar catálogo, confirmar atendimento) sejam acessíveis com o menor número possível de etapas e sem menus ambíguos.

#### Scenario: Conclusão de Ações em Poucos Cliques
- **WHEN** o cliente busca uma recomendação ou o prestador altera um status de atendimento
- **THEN** a interface responde imediatamente com atualização reativa do estado sem exigir recarregamentos manuais confusos
