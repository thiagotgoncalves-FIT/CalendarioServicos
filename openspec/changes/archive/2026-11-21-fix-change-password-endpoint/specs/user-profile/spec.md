## ADDED Requirements

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
