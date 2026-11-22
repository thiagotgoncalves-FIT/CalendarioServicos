# user-profile Specification

## Purpose
TBD - created by archiving change fix-change-password-endpoint. Update Purpose after archive.

## Requirements

### Requirement: Alteração Resiliente de Senha de Usuário
O sistema MUST permitir que qualquer usuário autenticado altere sua senha nas Configurações da Conta sem falhas provocadas por rotas inexistentes no backend Xano. Caso a rota remota retorne 404 ("Unable to locate request."), o sistema MUST aplicar a atualização de forma resiliente na base de dados de autenticação e na sessão.

#### Scenario: Alteração de Senha com Sucesso no Xano ou em Modo Resiliente
- **GIVEN** que o usuário está autenticado e preenche a senha atual correta e uma nova senha válida (mínimo 8 caracteres, letras e números)
- **WHEN** o usuário submete o formulário de alteração de senha
- **THEN** o sistema valida a conformidade dos dados, atualiza a senha (via endpoint ou fallback resiliente) e exibe mensagem de sucesso confirmando a alteração

#### Scenario: Prevenção de Erro "Unable to locate request."
- **GIVEN** que o backend Xano não possui o endpoint `/auth/change_password`
- **WHEN** o usuário tenta alterar sua senha
- **THEN** o sistema captura o código 404 e processa a atualização sem exibir o erro técnico "Unable to locate request." ao usuário

### Requirement: Recuperação de Senha com Exibição de Código no App
O sistema MUST exibir o código numérico de 6 dígitos de verificação diretamente na interface gráfica da aplicação ao solicitar a recuperação de senha, permitindo ao usuário confirmar o código e cadastrar sua nova senha sem dependência de envio de e-mails externos.

#### Scenario: Geração e Apresentação do Código na Tela
- **GIVEN** que o usuário informa seu e-mail na tela de recuperação de senha
- **WHEN** o usuário solicita a redefinição de senha
- **THEN** o sistema gera o código de 6 dígitos e o exibe com destaque na tela do aplicativo com campo para digitação e conferência

#### Scenario: Redefinição de Senha Bem-Sucedida
- **GIVEN** que o código de 6 dígitos está exibido na tela
- **WHEN** o usuário insere o código exibido e cadastra uma nova senha válida
- **THEN** o sistema atualiza a senha permanentemente e libera o acesso com a nova credencial

### Requirement: Persistência Durável de Alterações de Nome e Telefone
O sistema SHALL persistir permanentemente em disco e na sessão qualquer alteração de nome completo e telefone de contato realizada pelo usuário autenticado na tela de Configurações da Conta, garantindo que os novos dados cadastrais permaneçam válidos e visíveis após recarregamento da aplicação, navegação entre abas ou novo login.

#### Scenario: Atualização e persistência de nome e telefone nas configurações
- **WHEN** o usuário autenticado altera seu nome e/ou telefone na aba "Dados Cadastrais" e submete o formulário com dados válidos
- **THEN** o sistema SHALL gravar os novos dados cadastrais em arquivo persistente (`uploads/user_profiles.json`), atualizar a sessão ativa e exibir confirmação de sucesso sem reversão dos dados

#### Scenario: Carregamento dos dados cadastrais atualizados no login subsequente
- **WHEN** um usuário que alterou previamente seu nome ou telefone realiza logout e efetua novo login com suas credenciais
- **THEN** o sistema SHALL carregar o nome e telefone atualizados a partir do armazenamento persistente, exibindo os dados atualizados no cabeçalho e nas telas da aplicação

### Requirement: Design Visual com Abas Verticais, Ícones e Tipografia Cartoon
O sistema SHALL renderizar a interface de usuário com tipografia arredondada estilo cartoon (`Fredoka`/`Quicksand`), abas de navegação identificadas com ícones contextuais e dispostas verticalmente, e destaque em negrito proeminente (`font-weight: 800` ou superior) nos elementos cruciais de decisão (preços, status, notas e métricas).

#### Scenario: Exibição de abas com ícones e alinhamento vertical
- **WHEN** o usuário (prestador ou cliente) acessa seu painel ou as configurações da conta
- **THEN** o sistema SHALL exibir os nomes das abas acompanhados de seus respectivos ícones e organizados em disposição vertical, com indicador visual claro da aba selecionada

#### Scenario: Aplicação de tipografia cartoon e destaques em negrito
- **WHEN** qualquer tela da aplicação é carregada em modo Claro ou Escuro
- **THEN** o sistema SHALL carregar a tipografia arredondada em todos os componentes de texto e aplicar formatação em negrito destacada sobre preços monetários, notas de avaliação e status operacionais dos agendamentos
