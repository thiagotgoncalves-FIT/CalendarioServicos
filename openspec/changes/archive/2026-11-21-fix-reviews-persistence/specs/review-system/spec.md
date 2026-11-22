# review-system Specification (Delta)

## MODIFIED Requirements

### Requirement: Associação Obrigatória de Avaliação ao Serviço
Toda avaliação registrada na plataforma SHALL possuir vínculo obrigatório com o identificador do serviço (`servico_id`), do atendimento concluído (`agendamento_id`) e do cliente avaliador (`cliente_id`). O sistema SHALL rejeitar avaliações sem identificação de serviço e persistir as avaliações e status de atendimento de forma durável em disco local e/ou backend remoto.

#### Scenario: Registro de avaliação vinculada ao serviço do agendamento
- **WHEN** o cliente submete uma avaliação após a conclusão do atendimento
- **THEN** o sistema SHALL associar automaticamente o `servico_id` correspondente ao agendamento avaliado, persistindo nota, comentário, data e nome do cliente para exibição pública na janela de detalhes daquele serviço de forma durável em arquivo persistente (`uploads/reviews.json` e `uploads/reviewed_appointments.json`)

#### Scenario: Migração resiliente de avaliações legadas
- **WHEN** o sistema carrega avaliações pré-existentes que não possuem `servico_id` explicitamente gravado
- **THEN** o sistema SHALL enriquecer retroativamente cada registro com o identificador do serviço a partir dos agendamentos ou aplicar o serviço principal ativo como fallback seguro

#### Scenario: Bloqueio permanente de reavaliação pós-login
- **WHEN** o cliente titular que já avaliou um atendimento encerra a sessão e faz novo login na plataforma
- **THEN** o sistema SHALL consultar o registro persistente de atendimentos avaliados e NÃO DEVE exibir a janela modal de avaliação para o atendimento já avaliado
