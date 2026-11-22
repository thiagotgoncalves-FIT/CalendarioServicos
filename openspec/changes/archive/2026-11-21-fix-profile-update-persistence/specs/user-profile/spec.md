# user-profile Specification (Delta)

## ADDED Requirements

### Requirement: Persistência Durável de Alterações de Nome e Telefone
O sistema SHALL persistir permanentemente em disco e na sessão qualquer alteração de nome completo e telefone de contato realizada pelo usuário autenticado na tela de Configurações da Conta, garantindo que os novos dados cadastrais permaneçam válidos e visíveis após recarregamento da aplicação, navegação entre abas ou novo login.

#### Scenario: Atualização e persistência de nome e telefone nas configurações
- **WHEN** o usuário autenticado altera seu nome e/ou telefone na aba "Dados Cadastrais" e submete o formulário com dados válidos
- **THEN** o sistema SHALL gravar os novos dados cadastrais em arquivo persistente (`uploads/user_profiles.json`), atualizar a sessão ativa e exibir confirmação de sucesso sem reversão dos dados

#### Scenario: Carregamento dos dados cadastrais atualizados no login subsequente
- **WHEN** um usuário que alterou previamente seu nome ou telefone realiza logout e efetua novo login com suas credenciais
- **THEN** o sistema SHALL carregar o nome e telefone atualizados a partir do armazenamento persistente, exibindo os dados atualizados no cabeçalho e nas telas da aplicação
