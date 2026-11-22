# user-profile Specification (Delta)

## ADDED Requirements

### Requirement: Design Visual com Abas Verticais, Ícones e Tipografia Cartoon
O sistema SHALL renderizar a interface de usuário com tipografia arredondada estilo cartoon (`Fredoka`/`Quicksand`), abas de navegação identificadas com ícones contextuais e dispostas verticalmente, e destaque em negrito proeminente (`font-weight: 800` ou superior) nos elementos cruciais de decisão (preços, status, notas e métricas).

#### Scenario: Exibição de abas com ícones e alinhamento vertical
- **WHEN** o usuário (prestador ou cliente) acessa seu painel ou as configurações da conta
- **THEN** o sistema SHALL exibir os nomes das abas acompanhados de seus respectivos ícones e organizados em disposição vertical, com indicador visual claro da aba selecionada

#### Scenario: Aplicação de tipografia cartoon e destaques em negrito
- **WHEN** qualquer tela da aplicação é carregada em modo Claro ou Escuro
- **THEN** o sistema SHALL carregar a tipografia arredondada em todos os componentes de texto e aplicar formatação em negrito destacada sobre preços monetários, notas de avaliação e status operacionais dos agendamentos
