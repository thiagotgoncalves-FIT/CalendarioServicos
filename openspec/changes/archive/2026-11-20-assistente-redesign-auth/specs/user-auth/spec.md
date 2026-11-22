## ADDED Requirements

### Requirement: Fluxo Desacoplado de Autenticação em Páginas Exclusivas
O sistema MUST apresentar a tela de Login e a tela de Cadastro de forma totalmente segregada e independente, NÃO utilizando abas de alternância entre login e cadastro na mesma página. A página de Login MUST disponibilizar link com o texto "Não tem uma conta? Criar conta", que direciona o usuário para a página de cadastro. A página de Cadastro MUST disponibilizar link com o texto "Já tem uma conta? Entrar", que reconduz o usuário para a tela de login.

#### Scenario: Transição do Login para a Página Exclusiva de Cadastro
- **WHEN** o usuário não autenticado clica no link "Não tem uma conta? Criar conta" na tela de login
- **THEN** o sistema altera o estado de navegação e renderiza a tela dedicada de cadastro sem exibir o formulário de login

#### Scenario: Retorno da Página de Cadastro para o Login
- **WHEN** o usuário na página de cadastro clica no link "Já tem uma conta? Entrar"
- **THEN** o sistema altera o estado de navegação e renderiza exclusivamente a página de login

#### Scenario: Validação Obrigatória de Confirmação de Senha
- **WHEN** o usuário submete o formulário de cadastro com valores divergentes nos campos "Senha" e "Confirmação de Senha"
- **THEN** o sistema rejeita a operação com mensagem de erro clara informando que as senhas não coincidem, sem enviar a requisição ao Xano
