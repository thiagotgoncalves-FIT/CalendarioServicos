# service-catalog Specification

## Purpose
Permitir que o prestador de serviços gerencie seu portfólio comercial de atendimentos, definindo título, descrição, duração estimada em minutos e valor monetário cobrado.

## Requirements

### Requirement: Cadastro de Serviço pelo Prestador
O prestador autenticado DEVE conseguir cadastrar um novo serviço informando título, descrição (opcional), preço em reais e duração estimada em minutos.

#### Scenario: Cadastro de Serviço com Sucesso
- **WHEN** o prestador submete um serviço com título "Corte Degradê", preço R$ 45,00 e duração de 30 minutos
- **THEN** o sistema persiste o registro associado ao `prestador_id` do usuário logado e exibe o novo serviço na lista como ativo

#### Scenario: Tentativa de Cadastro com Preço ou Duração Inválidos
- **WHEN** o prestador tenta cadastrar um serviço com preço negativo ou duração igual/inferior a 0 minutos
- **THEN** o sistema rejeita a operação com erro de validação e orienta a correção dos campos numéricos

#### Scenario: Tentativa de Cadastro sem Título
- **WHEN** o prestador tenta salvar um serviço sem informar o título
- **THEN** o sistema impede a submissão e destaca a obrigatoriedade do título do serviço

---

### Requirement: Listagem e Gerenciamento de Serviços
O sistema DEVE permitir ao prestador visualizar todos os seus serviços cadastrados e alternar seu status de disponibilidade (ativo/inativo).

#### Scenario: Visualização do Catálogo pelo Prestador
- **WHEN** o prestador acessa a aba de serviços
- **THEN** o sistema exibe os cards de cada serviço contendo título, descrição, duração, preço formatado em BRL e indicador de status (ativo ou inativo)

#### Scenario: Desativação Temporária de Serviço
- **WHEN** o prestador opta por pausar a oferta de um serviço
- **THEN** o sistema atualiza o campo `ativo` para `false`, impedindo novos agendamentos desse item sem apagar o histórico

### Requirement: Interface Visual Refinada do Catálogo
O sistema DEVE apresentar os serviços do prestador em layout de cartões modernos ou tabela limpa, com badges estilizados de status (Ativo / Inativo), preço formatado no padrão monetário brasileiro (`R$ XX,XX`), duração em minutos, botão de ação para alternar status com feedback visual imediato e formulário expansível validado. Quando não houver serviços, o sistema DEVE exibir um estado vazio explicativo com atalho para inclusão do primeiro serviço.

#### Scenario: Visualização do Catálogo Vazio
- **WHEN** o prestador não possui nenhum serviço cadastrado em seu catálogo
- **THEN** o sistema exibe estado vazio amigável informando que nenhum serviço foi cadastrado e incentiva o cadastro do primeiro atendimento

#### Scenario: Validação e Feedback ao Salvar Serviço
- **WHEN** o prestador submete o formulário com dados válidos
- **THEN** o sistema exibe feedback de sucesso, atualiza a lista de serviços imediatamente e fecha o formulário
