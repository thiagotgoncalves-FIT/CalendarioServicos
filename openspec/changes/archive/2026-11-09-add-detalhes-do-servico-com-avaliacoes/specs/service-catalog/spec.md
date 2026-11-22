## ADDED Requirements

### Requirement: Janela Modal de Detalhes do Serviço no Catálogo Público
O sistema SHALL disponibilizar um botão "Detalhes" em cada card de serviço exibido no catálogo público. Ao ser acionado, o sistema SHALL abrir uma janela modal independente (`st.dialog`) exibindo as informações detalhadas e o histórico de avaliações exclusivo daquele serviço específico.

#### Scenario: Abertura da janela modal de detalhes do serviço
- **WHEN** o usuário clica no botão "Detalhes" de um card de serviço
- **THEN** o sistema SHALL abrir uma janela modal referente exclusivamente àquele serviço, apresentando de cima para baixo: nome do serviço, descrição completa, valor formatado em BRL, duração em minutos, resumo com nota média e total de avaliações, listagem cronológica das avaliações daquele serviço, botão para fechar a janela e botão para iniciar o fluxo de agendamento daquele serviço

#### Scenario: Visualização de serviço sem avaliações
- **WHEN** o usuário abre a janela de detalhes de um serviço que ainda não recebeu avaliações
- **THEN** o sistema SHALL exibir estado vazio acolhedor com a mensagem "Este serviço ainda não possui avaliações.", sem exibir erros ou valores nulos, mantendo o botão de agendamento disponível

