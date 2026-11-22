## ADDED Requirements

### Requirement: Sugestões Analíticas de Melhoria do Portfólio de Serviços
O sistema SHALL disponibilizar no painel financeiro a seção "Sugestões para o Portfólio", gerando indicadores analíticos e recomendações explicáveis para otimização comercial do catálogo com base nos dados reais de atendimentos concluídos e avaliações de clientes. O sistema SHALL ranquear os serviços por faturamento e volume de atendimentos, apresentar a participação percentual no faturamento total, o ticket médio e a nota média de cada item.

#### Scenario: Geração de sugestão para serviço de alta procura e excelente avaliação
- **WHEN** um serviço possui volume de atendimentos acima da média do catálogo e avaliação média igual ou superior a 4.5 estrelas
- **THEN** o sistema SHALL emitir sugestão explicável recomendando destacá-lo como carro-chefe na página inicial ou avaliar oportunidade de reajuste positivo de preço, apresentando explicitamente o percentual de faturamento e a nota média que motivaram a dica

#### Scenario: Geração de sugestão para serviço com baixa demanda
- **WHEN** um serviço ativo registra volume de atendimentos inferior a 10% da média do catálogo no período analisado
- **THEN** o sistema SHALL emitir sugestão explicável recomendando revisão do texto descritivo, promoção temporária ou criação de pacote/combo com outros serviços populares

#### Scenario: Alerta de atenção para serviço com avaliação baixa
- **WHEN** um serviço possui avaliações registradas com média inferior a 4.0 estrelas
- **THEN** o sistema SHALL apresentar alerta de atenção sugerindo análise detalhada dos feedbacks e revisão dos padrões de qualidade do serviço

#### Scenario: Detecção de períodos com menor ocupação de agenda
- **WHEN** a distribuição dos atendimentos revela dias da semana ou faixas de horário com ociosidade recorrente
- **THEN** o sistema SHALL sugerir campanhas de descontos ou promoções exclusivas para os dias e horários identificados como mais fracos

#### Scenario: Base insuficiente de dados para geração de sugestões
- **WHEN** o volume total de atendimentos concluídos no período for inferior ao limite mínimo de confiabilidade (mínimo de 3 atendimentos)
- **THEN** o sistema SHALL exibir mensagem transparente informando que a base de dados ainda é insuficiente para gerar sugestões seguras, evitando emitir conclusões precipitadas

