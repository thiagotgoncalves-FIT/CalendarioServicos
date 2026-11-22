## ADDED Requirements

### Requirement: Interface Visual Refinada do Catálogo
O sistema DEVE apresentar os serviços do prestador em layout de cartões modernos ou tabela limpa, com badges estilizados de status (Ativo / Inativo), preço formatado no padrão monetário brasileiro (`R$ XX,XX`), duração em minutos, botão de ação para alternar status com feedback visual imediato e formulário expansível validado. Quando não houver serviços, o sistema DEVE exibir um estado vazio explicativo com atalho para inclusão do primeiro serviço.

#### Scenario: Visualização do Catálogo Vazio
- **WHEN** o prestador não possui nenhum serviço cadastrado em seu catálogo
- **THEN** o sistema exibe estado vazio amigável informando que nenhum serviço foi cadastrado e incentiva o cadastro do primeiro atendimento

#### Scenario: Validação e Feedback ao Salvar Serviço
- **WHEN** o prestador submete o formulário com dados válidos
- **THEN** o sistema exibe feedback de sucesso, atualiza a lista de serviços imediatamente e fecha o formulário
