## Purpose

Fornece visão executiva consolidada e contextualizada da operação diária do prestador de serviços, com métricas precisas, formatação brasileira e estados vazios acolhedores.

## ADDED Requirements

### Requirement: Cabeçalho Contextual e Boas-Vindas
O sistema DEVE exibir no cabeçalho do painel uma saudação personalizada utilizando o nome real do usuário autenticado na sessão (`st.session_state["user"]`), acompanhado do nome da plataforma, perfil de acesso e da data corrente por extenso em português do Brasil (ex.: "18 de outubro de 2026").

#### Scenario: Visualização do Cabeçalho por Prestador Autenticado
- **WHEN** o prestador Hector Barros acessa o painel autenticado
- **THEN** o sistema exibe saudação nominal baseada em seu registro de usuário e a data de hoje formatada em pt-BR

### Requirement: Cartões de Métricas Resumo com Legendas Neutras
O sistema DEVE apresentar três cartões de métricas no topo da aba Resumo: "Agendamentos Hoje", "Serviços Ativos" e "Preço Médio". Todos os valores monetários DEVEM ser formatados no padrão monetário brasileiro (`R$ XX,XX`). As legendas ou indicadores secundários DEVEM ser estritamente descritivos e neutros, NÃO exibindo setas verdes de aumento ou variações de crescimento positivas quando os valores forem iguais a zero.

#### Scenario: Visualização de Métricas sem Agendamentos Hoje
- **WHEN** o prestador possui 0 agendamentos na data corrente
- **THEN** o cartão exibe "0", com legenda neutra explicativa (ex.: "Nenhum atendimento hoje") sem setas direcionais verdes de crescimento

#### Scenario: Formatação Monetária Brasileira de Preço Médio
- **WHEN** o preço médio do catálogo é calculado como 15.0
- **THEN** o valor é renderizado textualmente como "R$ 15,00"

### Requirement: Próximos Atendimentos do Dia com Estado Vazio
O sistema DEVE listar na aba Resumo os atendimentos previstos para o dia corrente. Quando não houver atendimentos para a data, o sistema DEVE apresentar uma mensagem de estado vazio amigável e encorajadora.

#### Scenario: Ausência de Atendimentos no Dia
- **WHEN** não há nenhum agendamento registrado para o prestador na data de hoje
- **THEN** o sistema exibe estado vazio claro com a mensagem "Você ainda não tem agendamentos hoje" e orientação rápida
