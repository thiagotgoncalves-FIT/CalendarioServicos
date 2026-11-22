# prestador-dashboard Specification

## Purpose
Fornece visão executiva consolidada e contextualizada da operação diária do prestador de serviços, com métricas precisas, formatação brasileira e estados vazios acolhedores.

## Requirements

### Requirement: Cabeçalho Contextual e Boas-Vindas
O sistema MUST exibir no cabeçalho do painel uma saudação personalizada utilizando o nome real do usuário autenticado na sessão (`st.session_state["user"]`), acompanhado do nome da plataforma, perfil de acesso e da data corrente por extenso em português do Brasil (ex.: "18 de outubro de 2026"). A barra lateral à esquerda MUST ser fixada permanentemente na interface, sem botões de recolhimento. Na tela de configurações da conta, o sistema MUST disponibilizar um único botão de retorno ao painel, evitando duplicidade de controles no topo da página.

#### Scenario: Visualização do Cabeçalho por Prestador Autenticado
- **WHEN** o prestador Hector Barros acessa o painel autenticado
- **THEN** o sistema exibe saudação nominal baseada em seu registro de usuário e a data de hoje formatada em pt-BR

#### Scenario: Navegação e Retorno Sem Duplicidade em Configurações
- **WHEN** o usuário estiver navegando na tela de Configurações da Conta
- **THEN** a interface exibe um único botão de retorno ("⬅️ Voltar") no cabeçalho da tela de configurações, sem exibir o botão superior redundante no topo da página

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

### Requirement: Exportação de Atendimentos em Formato CSV
O sistema MUST disponibilizar na aba Agenda do painel do prestador a funcionalidade de download dos atendimentos filtrados em formato CSV estruturado (Data, Horário, Cliente, Serviço, Duração, Preço e Status), permitindo ao prestador conciliação financeira e controle operacional externo.

#### Scenario: Download de Atendimentos Filtrados com Sucesso
- **WHEN** o prestador clica no botão de exportar agenda com atendimentos carregados
- **THEN** o sistema gera e disponibiliza para download um arquivo CSV codificado em UTF-8 com cabeçalhos legíveis em pt-BR e todos os registros correspondentes ao filtro ativo

#### Scenario: Tentativa de Exportação sem Atendimentos no Filtro
- **WHEN** a listagem de atendimentos filtrada estiver vazia
- **THEN** o sistema SHALL desabilitar o botão de download ou exibir aviso informativo amigável impedindo a geração de arquivo vazio

### Requirement: Contato Rápido e Lembrete via WhatsApp
O sistema MUST disponibilizar em cada card de atendimento confirmado na agenda um link de ação rápida para o WhatsApp do cliente (`https://wa.me/...`), com mensagem pré-formatada contendo os dados do agendamento (serviço, data e horário) para facilitar a comunicação e reduzir o risco de falta (no-show).

#### Scenario: Clique no Botão de WhatsApp do Atendimento
- **WHEN** o prestador clica na ação de WhatsApp de um atendimento com telefone válido registrado
- **THEN** o sistema abre em nova aba o link universal do WhatsApp direcionado para o número do cliente com a mensagem de confirmação do agendamento
