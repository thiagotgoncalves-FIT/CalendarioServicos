## Purpose

Permite que clientes descubram e contratem profissionais freelancers ideais por meio de um algoritmo inteligente de pontuação multicritério (0 a 100), com filtros estritos de orçamento e disponibilidade real de agenda.

## ADDED Requirements

### Requirement: Assistente de Recomendação Multicritério com Pontuação Normalizada
O sistema MUST disponibilizar um assistente inteligente onde o cliente informa o serviço desejado, descrição da necessidade, orçamento máximo e data/período pretendido. O sistema SHALL calcular uma pontuação normalizada de 0 a 100 para cada prestador elegível com base em pesos transparentes: compatibilidade do serviço/descrição (peso 35%), aderência ao orçamento (peso 25%), disponibilidade de agenda na data (peso 25%) e avaliação média do profissional (peso 15%).

#### Scenario: Geração de Recomendações Ordenadas por Score
- **WHEN** o cliente submete seus critérios de busca informando serviço, orçamento e data válida
- **THEN** o sistema retorna a lista de prestadores compatíveis ordenada decrescentemente pela pontuação final calculada de 0 a 100

#### Scenario: Justificativa Transparente dos Fatores de Recomendação
- **WHEN** os prestadores recomendados são exibidos na tela
- **THEN** cada card de profissional apresenta indicadores descritivos claros dos fatores que compuseram sua nota (ex.: "Dentro do orçamento", "Horário livre confirmado", "Alta compatibilidade com a descrição")

### Requirement: Filtros Excludentes Obrigatórios de Orçamento e Disponibilidade Real
O sistema MUST aplicar filtros excludentes obrigatórios antes do cálculo de ordenação. Nenhum prestador com valor de serviço superior ao orçamento máximo informado ou sem horários livres confirmados na data selecionada SHALL figurar na listagem de recomendações. O sistema NÃO DEVE gerar dados fictícios ou simulações enganosas na ausência de correspondência exata.

#### Scenario: Exclusão de Prestadores Acima do Orçamento
- **WHEN** o prestador oferece o serviço solicitado por um valor de R$ 120,00 e o cliente definiu o teto de R$ 100,00
- **THEN** o sistema exclui sumariamente o prestador da lista de recomendações

#### Scenario: Exclusão de Prestador Sem Disponibilidade na Data
- **WHEN** o prestador atende ao serviço e ao orçamento, mas todos os seus slots de atendimento para a data selecionada estão ocupados ou fora do expediente
- **THEN** o sistema desclassifica o prestador dos resultados daquela data

#### Scenario: Tratamento Acolhedor de Ausência de Resultados
- **WHEN** nenhum prestador atende simultaneamente aos filtros de serviço, orçamento e data
- **THEN** o sistema exibe estado vazio claro e amigável orientando o cliente a flexibilizar a data ou o valor máximo para encontrar opções

### Requirement: Início Direto de Agendamento a partir da Recomendação
O sistema MUST disponibilizar em cada card de prestador recomendado uma ação direta para visualizar os slots disponíveis e efetivar a reserva do serviço utilizando o motor de agendamentos existente.

#### Scenario: Seleção e Reserva a partir da Recomendação
- **WHEN** o cliente clica no botão "Agendar com este Profissional" no card de recomendação
- **THEN** o sistema abre a seleção de horários disponíveis daquele prestador na data pesquisada e conclui a reserva com confirmação imediata
