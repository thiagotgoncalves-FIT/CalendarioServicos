## ADDED Requirements

### Requirement: Painel de Atendimentos com Filtros e Ações Rápidas
O sistema DEVE prover na aba Agenda de Atendimentos filtros simultâneos por status (`Todos`, `confirmado`, `pendente`, `concluido`, `cancelado`) e por data específica, exibição de cards informativos com badges de status padronizadas por cores semânticas e botões de ação rápida para concluir ou cancelar atendimentos com confirmação e sem erros de execução. Em caso de ausência de registros correspondentes aos filtros, o sistema DEVE apresentar estado vazio amigável.

#### Scenario: Filtragem sem Resultados Encontrados
- **WHEN** o prestador seleciona um filtro de status ou data sem atendimentos cadastrados
- **THEN** o sistema exibe estado vazio claro indicando que não há agendamentos para os critérios selecionados

#### Scenario: Transição de Status com Atualização Visual
- **WHEN** o prestador clica em "Concluir" ou "Cancelar" em um agendamento
- **THEN** o sistema atualiza o status no backend, exibe toast/mensagem de sucesso e reflete a mudança instantaneamente
