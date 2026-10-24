## ADDED Requirements

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
