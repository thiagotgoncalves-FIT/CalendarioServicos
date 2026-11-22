## MODIFIED Requirements

### Requirement: Cadastro de Usuário com Seleção de Perfil
O sistema DEVE permitir que um novo usuário se cadastre informando nome, e-mail válido, senha segura (mínimo 8 caracteres com ao menos 1 letra e 1 dígito), telefone e o perfil de acesso desejado (`prestador` ou `cliente`). O sistema DEVE persistir os dados na tabela `user` do Xano com senha armazenada como hash seguro via mecanismo nativo do Xano. O sistema NÃO DEVE recorrer a bypass ou mock em memória quando a API do Xano estiver ativa e retornar resposta válida.

#### Scenario: Cadastro de Prestador de Serviços com Sucesso
- **WHEN** o usuário submete o formulário de cadastro com nome, e-mail válido, senha com 8+ caracteres e ao menos 1 letra e 1 dígito, telefone e seleciona o perfil "prestador"
- **THEN** o sistema cria o registro na tabela `user` do Xano com senha armazenada como hash, retorna `authToken` JWT válido e dados básicos do usuário (sem campo `password`)

#### Scenario: Cadastro de Cliente com Sucesso
- **WHEN** o usuário submete o formulário de cadastro com credenciais válidas e seleciona o perfil "cliente"
- **THEN** o sistema cria o registro no Xano, retorna `authToken` JWT e dados do usuário com `role` definido como "cliente"

#### Scenario: Tentativa de Cadastro com E-mail Já Existente
- **WHEN** o usuário tenta cadastrar uma conta com um endereço de e-mail que já está registrado na tabela `user` do Xano
- **THEN** o sistema rejeita a operação com código de erro 400 ou 409 e exibe mensagem clara informando que o e-mail já está em uso

#### Scenario: Tentativa de Cadastro com Senha Fraca
- **WHEN** o usuário submete uma senha com menos de 8 caracteres ou sem ao menos 1 letra e 1 dígito
- **THEN** o sistema rejeita a operação com mensagem indicando o critério mínimo de senha exigido

#### Scenario: Tentativa de Cadastro com Campos Obrigatórios Ausentes
- **WHEN** o usuário submete o formulário com campos essenciais em branco (nome, e-mail ou senha)
- **THEN** o sistema impede a submissão e apresenta mensagem de validação

#### Scenario: Tentativa de Cadastro com Xano Indisponível
- **WHEN** o usuário submete o formulário e a API do Xano não responde ou retorna erro 5xx
- **THEN** o sistema rejeita a operação com mensagem de indisponibilidade do serviço e NÃO aprova o cadastro via mock em memória

### Requirement: Autenticação de Usuário e Emissão de Token
O sistema DEVE autenticar o usuário a partir de e-mail e senha validando contra a tabela `user` do Xano usando verificação segura de hash de senha nativa do Xano. A autenticação DEVE ser realizada estritamente contra o backend do Xano. O sistema NÃO DEVE emitir tokens mock locais quando a API do Xano estiver ativa.

#### Scenario: Login com Credenciais Válidas
- **WHEN** o usuário insere e-mail e senha corretos correspondentes a um registro na tabela `user` do Xano
- **THEN** o sistema valida o hash da senha no Xano, retorna `authToken` JWT válido e dados do usuário (nome, e-mail, role) sem expor o campo `password`

#### Scenario: Login com Senha Incorreta
- **WHEN** o usuário insere um e-mail cadastrado mas com a senha incorreta
- **THEN** o sistema rejeita o login com mensagem de erro amigável sem expor detalhes internos ou hashes

#### Scenario: Login com E-mail Inexistente
- **WHEN** o usuário tenta logar com um e-mail não cadastrado na tabela `user` do Xano
- **THEN** o sistema rejeita a autenticação com mensagem genérica de credenciais inválidas

#### Scenario: Login com Xano Indisponível
- **WHEN** o usuário tenta realizar o login e o serviço Xano não está acessível (timeout, 5xx)
- **THEN** o sistema exibe mensagem de falha de conexão e NÃO emite um mock JWT local
