## Why

Atualmente, o prestador autônomo (barbeiro/administrador) não possui uma visão consolidada de faturamento diário por período nem indicadores analíticos sobre o desempenho dos seus serviços. Para tomar decisões financeiras e comerciais informadas (como ajustar preços, destacar serviços procurados, criar combos ou lançar promoções para horários ociosos), ele precisa de uma área restrita e confiável que calcule o faturamento real com base exclusivamente em atendimentos concluídos e sugira melhorias explicáveis para o seu portfólio.

## What Changes

- **Aba Financeiro e Relatórios no Painel do Prestador**:
  - Nova aba "Financeiro" integrada ao painel exclusivo do prestador logado (`role == "prestador"`).
  - Bloqueio estrito de acesso e visualização para clientes e visitantes não autenticados (frontend e camada de serviço).
  - Cada prestador autenticado visualiza exclusivamente os dados financeiros dos seus próprios atendimentos.
- **Faturamento Diário e Indicadores**:
  - Cálculo de receita considerando **SOMENTE atendimentos concluídos** (`status == 'concluido'`). Atendimentos cancelados, faltas ou pendentes são descartados do faturamento.
  - Imutabilidade do valor histórico: utiliza o `valor_cobrado` persistido no momento do atendimento, garantindo que alterações posteriores de preço no catálogo não afetem o faturamento passado.
  - Resumo financeiro do período com 4 cartões de métricas: Total Faturado (R$), Quantidade de Atendimentos Concluídos, Ticket Médio (R$) e Comparação percentual com o período anterior equivalente.
  - Filtros rápidos por período: Hoje, Ontem, Últimos 7 dias, Últimos 30 dias, Mês Atual e Intervalo Personalizado (seleção de data inicial e final).
  - Visualização gráfica diária do faturamento (gráfico de barras/linhas) no período selecionado.
  - Tabela/lista diária com data, faturamento total do dia, total de atendimentos e ticket médio do dia.
  - Detalhamento interativo por dia: ao selecionar uma data específica, exibe a relação dos atendimentos concluídos naquele dia (horário, cliente, serviço contratado e valor cobrado).
  - Estado vazio amigável quando não houver atendimentos concluídos no intervalo consultado.
  - Formatação monetária rigorosa em Real brasileiro (`R$ XX,XX`), datas em pt-BR e respeito ao fuso horário de Brasília (`America/Sao_Paulo`).
- **Sugestões Orientadas a Dados para o Portfólio de Serviços**:
  - Seção integrada "Sugestões para o Portfólio" no painel financeiro.
  - Ranking de serviços por faturamento gerado e volume de atendimentos concluídos.
  - Indicadores cruzados por serviço: nota média das avaliações dos clientes, ticket médio praticado e participação percentual (%) no faturamento total do período.
  - Motor de regras determinísticas e explicáveis:
    - *Alta procura e nota alta (≥ 4.5)*: sugerir destacar na vitrine principal ou avaliar oportunidade de aumento de preço.
    - *Baixa procura (< 10% da média do catálogo)*: sugerir promoção temporária, revisão da descrição/título ou inclusão em combo promocional.
    - *Nota média baixa (< 4.0)*: alertar para revisar a qualidade da execução e analisar comentários e feedbacks dos clientes.
    - *Dias e horários fracos da semana*: identificar períodos com menor ocupação de agenda e sugerir promoções direcionadas para esses horários ociosos.
  - Transparência total: cada sugestão apresenta a justificativa clara com os dados reais que a fundamentaram.
  - Proteção contra amostras insuficientes: se houver poucos dados (ex.: menos de 3 atendimentos concluídos no período), exibe mensagem informativa orientando que mais atendimentos são necessários para sugestões confiáveis.
  - Caráter puramente informativo: o sistema não altera preços nem serviços automaticamente.

## Capabilities

### New Capabilities
*(Nenhuma nova capability isolada necessária; o comportamento estende as capabilities de gestão do prestador e inteligência de catálogo existentes)*

### Modified Capabilities
- `prestador-dashboard`: Adiciona a aba "Financeiro", controle de acesso restrito a prestadores, cálculo de faturamento diário sobre atendimentos concluídos, filtros por período, gráfico de faturamento dia a dia e detalhamento por dia.
- `service-catalog`: Adiciona os indicadores de desempenho comercial dos serviços e o motor de sugestões analíticas explicáveis para o catálogo e portfólio.

## Impact

- **Frontend (`app.py`)**:
  - Adição da aba "Financeiro" no conjunto de abas do Prestador (`st.tabs`).
  - Renderização dos filtros de período, cartões de métricas, gráfico diário de faturamento e expansor de detalhamento por data.
  - Renderização da seção de sugestões do portfólio com badges explicativos e rankings.
- **Camada de Serviços (`services/financial_service.py` ou expansão em `appointment_service.py` / `analytics_service.py`)**:
  - Criação de módulo de análise financeira `services/financial_service.py` com funções dedicadas para agregação de faturamento diário, filtros temporais e regras determinísticas de sugestão de portfólio.
- **Modelos de Dados e Persistência**:
  - Consumo seguro dos campos `valor_cobrado`, `status`, `data` e `hora_inicio` dos atendimentos.
  - Fallback automático para atendimentos legados que não possuam `valor_cobrado` preenchido.

