## ADDED Requirements

### Requirement: Avaliação de Atendimento Concluído pelo Cliente
O sistema SHALL permitir que o cliente autenticado avalie um atendimento com status `concluido` diretamente a partir da aba "Meus Agendamentos", garantindo que cada atendimento seja avaliado no máximo uma única vez e exclusivamente pelo cliente titular da reserva.

#### Scenario: Avaliação de atendimento concluído com sucesso
- **WHEN** o cliente autenticado acessa "Meus Agendamentos", localiza um atendimento com status `concluido` ainda não avaliado e submete nota e comentário válidos
- **THEN** o sistema SHALL registrar a avaliação vinculada ao atendimento, marcar o atendimento como avaliado e exibir badge de confirmação

#### Scenario: Tentativa de reavaliação de atendimento já avaliado
- **WHEN** o cliente visualiza um atendimento com status `concluido` que já foi previamente avaliado
- **THEN** o sistema SHALL ocultar o formulário de avaliação ou desabilitar novas submissões, exibindo a nota previamente atribuída

#### Scenario: Tentativa de avaliar atendimento pendente ou confirmado
- **WHEN** o cliente consulta um atendimento com status diferente de `concluido`
- **THEN** o sistema SHALL não disponibilizar a ação de avaliação

## MODIFIED Requirements

### Requirement: Painel de Atendimentos com Filtros e Ações Rápidas
O sistema SHALL prover nas visões de agenda do prestador e do cliente filtros simultâneos por status (`Todos`, `confirmado`, `pendente`, `concluido`, `cancelado`) e por data específica, com exibição de cards limpos e sem exposição de identificadores internos técnicos de banco de dados (ex: `Agendamento #...` ou `Cliente #...`). Os cards SHALL utilizar badges de status padronizadas com cores semânticas amigáveis, formatação monetária e de datas em padrão brasileiro (pt-BR) e botões de ação com linguagem humanizada para concluir ou cancelar agendamentos. Em caso de ausência de registros correspondentes aos filtros, o sistema SHALL apresentar estado vazio acolhedor e informativo.

#### Scenario: Filtragem sem Resultados Encontrados
- **WHEN** o usuário seleciona um filtro de status ou data sem agendamentos cadastrados
- **THEN** o sistema SHALL exibir estado vazio claro indicando que não há agendamentos para os critérios selecionados

#### Scenario: Transição de Status com Atualização Visual
- **WHEN** o prestador clica em "Concluir" ou "Cancelar" em um agendamento
- **THEN** o sistema SHALL atualizar o status do agendamento, recarregar a visualização e exibir notificação de confirmação (toast) amigável

#### Scenario: Apresentação simplificada sem termos de desenvolvedor
- **WHEN** os agendamentos são renderizados na interface do cliente ou do prestador
- **THEN** o sistema SHALL exibir apenas o nome do serviço, nome da outra parte, data, horário e valor formatados, sem expor chaves primárias, hashes técnicos ou jargões de sistema

