## Purpose

Permite que clientes visualizem a nota média e depoimentos específicos de cada serviço e enviem avaliações para atendimentos concluídos através de janela modal, assegurando o vínculo obrigatório com o serviço e a unicidade da avaliação.

## ADDED Requirements

### Requirement: Associação Obrigatória de Avaliação ao Serviço
Toda avaliação registrada na plataforma SHALL possuir vínculo obrigatório com o identificador do serviço (`servico_id`), do atendimento concluído (`agendamento_id`) e do cliente avaliador (`cliente_id`). O sistema SHALL rejeitar avaliações sem identificação de serviço.

#### Scenario: Registro de avaliação vinculada ao serviço do agendamento
- **WHEN** o cliente submete uma avaliação após a conclusão do atendimento
- **THEN** o sistema SHALL associar automaticamente o `servico_id` correspondente ao agendamento avaliado, persistindo nota, comentário, data e nome do cliente para exibição pública na janela de detalhes daquele serviço

#### Scenario: Migração resiliente de avaliações legadas
- **WHEN** o sistema carrega avaliações pré-existentes que não possuem `servico_id` explicitamente gravado
- **THEN** o sistema SHALL enriquecer retroativamente cada registro com o identificador do serviço a partir dos agendamentos ou aplicar o serviço principal ativo como fallback seguro

### Requirement: Janela Modal de Avaliação Pós-Atendimento
Quando um agendamento for concluído pelo prestador, o sistema SHALL disponibilizar ao cliente titular uma janela modal solicitando a avaliação daquele atendimento concluído.

#### Scenario: Exibição da janela modal de avaliação para atendimento concluído
- **WHEN** o cliente autenticado acessa a plataforma e possui atendimento com status "concluido" que ainda não foi avaliado
- **THEN** o sistema SHALL exibir uma janela modal contendo o nome do serviço contratado (identificado automaticamente), seleção obrigatória de 1 a 5 estrelas, campo de comentário de até 500 caracteres, botão de envio e opção de fechar/avaliar mais tarde

#### Scenario: Fechamento da janela sem submissão
- **WHEN** o cliente fecha a janela modal sem submeter a avaliação
- **THEN** o sistema SHALL manter o agendamento no estado pendente de avaliação e disponibilizar um botão "Avaliar Atendimento" no card do agendamento na aba "Meus Agendamentos" para permitir envio futuro

#### Scenario: Bloqueio de reavaliação após envio bem-sucedido
- **WHEN** o cliente submete a avaliação com sucesso
- **THEN** o sistema SHALL registrar a avaliação, marcar o agendamento como avaliado, exibir feedback de sucesso e impedir qualquer nova submissão para aquele mesmo atendimento

### Requirement: Métricas e Paginação de Avaliações por Serviço
O sistema SHALL calcular a nota média e o total de avaliações de forma isolada para cada serviço e permitir carregamento progressivo dos depoimentos.

#### Scenario: Cálculo de métricas isoladas por serviço
- **WHEN** as avaliações de um serviço específico são consultadas
- **THEN** o sistema SHALL calcular a nota média (arredondada para 1 casa decimal) e o total considerando apenas as avaliações que possuem o `servico_id` correspondente

#### Scenario: Carregamento progressivo de avaliações do serviço
- **WHEN** a quantidade de avaliações de um serviço ultrapassa o limite inicial de exibição
- **THEN** o sistema SHALL disponibilizar controle de "Carregar Mais" para exibir as avaliações adicionais ordenadas da mais recente para a mais antiga

### Requirement: Exibição Contextual Exclusiva por Serviço
As avaliações e notas médias SHALL ser exibidas exclusivamente vinculadas aos seus respectivos serviços (na janela modal de Detalhes do serviço no catálogo e no bloco de avaliação dos resultados da pesquisa de serviços), sem a disponibilização de uma aba genérica de avaliações.

#### Scenario: Consulta contextualizada sem aba geral
- **WHEN** o usuário navega pela plataforma
- **THEN** o sistema SHALL omitir a aba geral autônoma de avaliações e apresentar as notas e depoimentos apenas dentro do modal de detalhes de cada serviço no catálogo e no resumo de avaliações do assistente de recomendação

