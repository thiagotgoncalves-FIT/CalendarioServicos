## Purpose

Permite que clientes visualizem depoimentos, notas e a média de satisfação geral dos atendimentos prestados, promovendo transparência e confiança pública na plataforma AgendAí.

## ADDED Requirements

### Requirement: Exibição Pública de Avaliações e Métricas Consolidadas
O sistema SHALL disponibilizar uma seção pública de Avaliações acessível a todos os usuários, apresentando o cálculo consolidado da nota média geral (em escala de 1.0 a 5.0 estrelas), o total de avaliações recebidas e a listagem dos depoimentos cadastrados.

#### Scenario: Visualização de métricas e lista de avaliações existentes
- **WHEN** o usuário acessa a aba pública de avaliações e existem avaliações cadastradas
- **THEN** o sistema SHALL exibir o card de resumo com a nota média formatada com 1 casa decimal, total de avaliações, e a lista de cards contendo nota em estrelas, data formatada em pt-BR, primeiro nome do cliente (com inicial do sobrenome) e comentário

#### Scenario: Visualização quando não há avaliações cadastradas
- **WHEN** o usuário acessa a aba de avaliações e não existe nenhuma avaliação registrada
- **THEN** o sistema SHALL exibir um estado vazio amigável informando que ainda não há avaliações cadastradas, sem exibir valores nulos ou erros de execução

### Requirement: Ordenação e Paginação de Avaliações
O sistema SHALL apresentar as avaliações ordenadas cronologicamente a partir das mais recentes e prover mecanismo de paginação ou carregamento progressivo para evitar sobrecarga visual.

#### Scenario: Ordenação cronológica decrescente
- **WHEN** a listagem de avaliações é carregada
- **THEN** o sistema SHALL apresentar em primeiro lugar as avaliações com data de envio mais recente

#### Scenario: Paginação de avaliações
- **WHEN** o volume total de avaliações ultrapassa o limite padrão de exibição inicial (ex: 5 avaliações)
- **THEN** o sistema SHALL disponibilizar controles de navegação ou botão de carregar mais avaliações

### Requirement: Validação e Submissão de Avaliação
O sistema SHALL validar a submissão de avaliações exigindo obrigatoriamente a seleção de nota inteira entre 1 e 5 estrelas e comentário textual de até 500 caracteres, rejeitando submissões vazias ou inválidas.

#### Scenario: Submissão com dados válidos
- **WHEN** o cliente informa uma nota entre 1 e 5 estrelas e um comentário válido de até 500 caracteres e clica em enviar
- **THEN** o sistema SHALL persistir a avaliação, recalcular a média geral e exibir confirmação de sucesso com mensagem amigável

#### Scenario: Tentativa de envio com nota não preenchida
- **WHEN** o cliente tenta submeter o formulário sem selecionar uma nota válida
- **THEN** o sistema SHALL bloquear a gravação e exibir mensagem clara solicitando a atribuição da nota

