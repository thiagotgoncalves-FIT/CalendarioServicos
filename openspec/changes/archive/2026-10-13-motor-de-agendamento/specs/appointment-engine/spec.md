## Purpose

Provê o motor central de agendamentos do AgendAí, calculando horários livres a partir da grade de atendimento do prestador, prevenindo double-booking e gerenciando o ciclo de vida das reservas.

## ADDED Requirements

### Requirement: Cálculo e Geração de Slots Livres
O sistema DEVE calcular dinamicamente os horários de início disponíveis (slots) para uma data selecionada pelo cliente, respeitando a grade semanal do prestador, o intervalo de almoço e a duração necessária do serviço em blocos de 30 minutos.

#### Scenario: Geração de slots em dia útil com expediente ativo
- **WHEN** o cliente seleciona uma data correspondente a um dia de trabalho do prestador e um serviço de 45 minutos
- **THEN** o sistema SHALL retornar apenas os horários de início cujo bloco de duração caiba integralmente no expediente e não colida com o intervalo de almoço ou agendamentos existentes

#### Scenario: Bloqueio de horários no passado para a data corrente
- **WHEN** o cliente seleciona o dia atual
- **THEN** o sistema SHALL filtrar e ocultar todos os slots de horários cujo início seja anterior ou igual ao momento atual

#### Scenario: Dia sem expediente configurado
- **WHEN** o cliente seleciona uma data na qual o prestador marcou o dia como inativo na sua grade
- **THEN** o sistema SHALL retornar uma lista vazia de slots e indicar indisponibilidade de atendimento para a data

### Requirement: Prevenção de Conflito de Horários (Anti-Double-Booking)
O sistema SHALL impedir a criação de qualquer agendamento cujo intervalo de atendimento colida com outro agendamento já existente com status `pendente` ou `confirmado` para o mesmo prestador.

#### Scenario: Tentativa de agendar em horário já reservado
- **WHEN** o cliente tenta confirmar uma reserva para um horário que colide com outro agendamento ativo
- **THEN** o sistema SHALL rejeitar a solicitação, emitir mensagem de conflito e atualizar a lista de slots disponíveis

#### Scenario: Liberação de horário após cancelamento
- **WHEN** um agendamento existente é cancelado pelo cliente ou pelo prestador
- **THEN** o sistema SHALL liberar imediatamente o respectivo horário para novas consultas de disponibilidade

### Requirement: Criação e Confirmação de Reserva pelo Cliente
O sistema SHALL permitir que um usuário autenticado com perfil `cliente` selecione um serviço ativo, uma data e um slot livre para registrar um novo agendamento.

#### Scenario: Agendamento criado com sucesso
- **WHEN** o cliente escolhe um serviço válido, seleciona uma data e um slot disponível e confirma a operação
- **THEN** o sistema SHALL registrar o agendamento associando cliente, prestador e serviço, gravando o valor cobrado e o status inicial como `confirmado`

### Requirement: Gerenciamento de Status pelo Prestador e Cliente
O sistema SHALL permitir a consulta dos agendamentos filtrados por perfil e a atualização de seu estado (`confirmado`, `concluido`, `cancelado`).

#### Scenario: Prestador visualiza e conclui atendimento
- **WHEN** o prestador autenticado acessa sua agenda de atendimentos e aciona a conclusão de um agendamento confirmado
- **THEN** o sistema SHALL atualizar o status para `concluido` e refletir a mudança nas métricas e na listagem

#### Scenario: Cliente cancela agendamento futuro
- **WHEN** o cliente autenticado acessa "Meus Agendamentos" e solicita o cancelamento de uma reserva futura
- **THEN** o sistema SHALL atualizar o status para `cancelado` e disponibilizar o slot para novos agendamentos
