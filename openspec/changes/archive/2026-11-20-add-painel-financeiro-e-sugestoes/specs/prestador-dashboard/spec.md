## ADDED Requirements

### Requirement: Painel de Faturamento Diário e Métricas Financeiras
O sistema SHALL disponibilizar no painel do prestador uma área dedicada de gestão financeira que consolida a receita obtida exclusivamente a partir de atendimentos com status "concluido". Atendimentos cancelados, pendentes ou não realizados SHALL ser expressamente desconsiderados do cálculo de faturamento. O valor atribuído a cada atendimento SHALL ser o `valor_cobrado` registrado no momento do agendamento, preservando a imutabilidade histórica frente a eventuais alterações posteriores na tabela de preços dos serviços.

#### Scenario: Cálculo de faturamento estritamente com atendimentos concluídos
- **WHEN** o prestador consulta o painel financeiro para um determinado período
- **THEN** o sistema SHALL somar apenas os valores dos atendimentos com status "concluido", exibindo o total faturado formatado em BRL (`R$ XX,XX`), a contagem total de atendimentos concluídos, o ticket médio e a variação comparativa em relação ao período anterior correspondente

#### Scenario: Preservação histórica do valor cobrado
- **WHEN** o preço de um serviço no catálogo for modificado de R$ 50,00 para R$ 70,00
- **THEN** os atendimentos previamente concluídos daquele serviço SHALL continuar computando R$ 50,00 no faturamento histórico e diário

#### Scenario: Visualização de período sem atendimentos concluídos
- **WHEN** o prestador seleciona um período que não possui atendimentos com status "concluido"
- **THEN** o sistema SHALL exibir estado vazio informativo acolhedor, com valores zerados e mensagem clara de ausência de faturamento no período, sem gerar erros de execução ou divisões por zero

### Requirement: Filtros Temporais e Detalhamento Diário
O sistema SHALL fornecer seletores de intervalo temporal incluindo: Hoje, Ontem, Últimos 7 dias, Últimos 30 dias, Mês Atual e Intervalo Personalizado (com seleção de data inicial e final respeitando o fuso de Brasília). Para o período ativo, o sistema SHALL renderizar um gráfico de faturamento diário (barras ou linhas), uma listagem cronológica com os totais de cada dia e um mecanismo de detalhamento interativo que exibe os atendimentos individuais (horário, serviço e valor cobrado) da data selecionada.

#### Scenario: Filtragem por período e renderização gráfica
- **WHEN** o prestador seleciona o filtro "Últimos 7 dias"
- **THEN** o sistema SHALL atualizar os indicadores agregados, renderizar o gráfico com as barras diárias de faturamento dos últimos 7 dias e listar a tabela diária ordenada por data

#### Scenario: Detalhamento de atendimentos de uma data específica
- **WHEN** o prestador seleciona ou expande um dia específico na listagem financeira
- **THEN** o sistema SHALL apresentar a listagem completa dos atendimentos concluídos daquele dia, informando hora de início, nome do serviço e valor faturado de cada um

### Requirement: Controle de Acesso Restrito ao Painel Financeiro
O painel financeiro, suas métricas agregadas e o detalhamento de faturamento SHALL ser de acesso estritamente restrito a usuários autenticados com papel (`role`) de "prestador". Clientes e usuários anônimos SHALL NÃO ter acesso à interface nem aos dados de faturamento. O sistema SHALL assegurar que cada prestador acesse exclusivamente as métricas e atendimentos vinculados ao seu próprio identificador (`prestador_id`).

#### Scenario: Acesso permitido para prestador autenticado
- **WHEN** um usuário autenticado com perfil de prestador acessa a aba "Financeiro"
- **THEN** o sistema SHALL carregar e apresentar apenas os dados financeiros relativos aos seus próprios atendimentos

#### Scenario: Bloqueio absoluto para perfil de cliente
- **WHEN** um usuário autenticado com perfil de cliente navega pela plataforma
- **THEN** o sistema SHALL omitir a aba de financeiro e rejeitar qualquer tentativa de acesso aos dados de receita do prestador

