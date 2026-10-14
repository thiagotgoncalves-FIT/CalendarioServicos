## MODIFIED Requirements

### Requirement: Cadastro de Usuário com Seleção de Perfil
O sistema DEVE permitir que um novo usuário se cadastre informando nome, e-mail válido, senha segura, telefone e o perfil de acesso desejado (`prestador` ou `cliente`). O sistema DEVE persistir os dados exclusivamente na API do Xano e NÃO DEVE recorrer a bypasses ou mocks em memória caso a API esteja indisponível.

#### Scenario: Cadastro de Prestador de Serviços com Sucesso
- **WHEN** o usuário submete o formulário de cadastro com nome "Carlos Barbeiro", e-mail "carlos@barbearia.com", senha válida, telefone e seleciona o perfil "prestador"
- **THEN** o sistema cria o registro na tabela de usuários do Xano, gera o hash seguro da senha e retorna confirmação de sucesso com token de autenticação e papel definido como prestador

#### Scenario: Cadastro de Cliente com Sucesso
- **WHEN** o usuário submete o formulário de cadastro com nome "Mariana Silva", e-mail "mariana@email.com", senha válida, telefone e seleciona o perfil "cliente"
- **THEN** o sistema cria o registro com sucesso no Xano e atribui o papel de cliente

#### Scenario: Tentativa de Cadastro com E-mail Já Existente
- **WHEN** o usuário tenta cadastrar uma conta com um endereço de e-mail que já está registrado no sistema (Xano)
- **THEN** o sistema rejeita a operação com código de erro 400/409 e exibe uma mensagem clara informando que o e-mail já está em uso

#### Scenario: Tentativa de Cadastro com Campos Obrigatórios Ausentes
- **WHEN** o usuário submete o formulário com campos essenciais em branco (nome, e-mail ou senha)
- **THEN** o sistema impede a submissão e destaca os campos que necessitam de preenchimento

#### Scenario: Tentativa de Cadastro com Xano Indisponível
- **WHEN** o usuário submete o formulário e a API do Xano não responde ou retorna erro 503
- **THEN** o sistema rejeita a operação com uma mensagem de erro indicando indisponibilidade do serviço e NÃO aprova o cadastro via mock em memória

### Requirement: Autenticação de Usuário e Emissão de Token
O sistema DEVE autenticar o usuário a partir de suas credenciais (e-mail e senha) e emitir um token JWT para identificação das requisições subsequentes. A autenticação DEVE ser realizada estritamente contra o backend do Xano, bloqueando logins via fallback em memória (mock).

#### Scenario: Login com Credenciais Válidas
- **WHEN** o usuário insere seu e-mail e senha corretos e clica em "Entrar"
- **THEN** o sistema valida as credenciais no Xano, retorna o token de autenticação JWT, os dados do usuário (nome, e-mail, role) e o direciona para a área correspondente ao seu perfil

#### Scenario: Login com Senha Incorreta
- **WHEN** o usuário insere um e-mail cadastrado no Xano, mas com a senha incorreta
- **THEN** o sistema rejeita o login com código 401/403 e apresenta mensagem de erro amigável sem expor detalhes internos

#### Scenario: Login com E-mail Inexistente
- **WHEN** o usuário tenta logar com um e-mail não cadastrado na base do Xano
- **THEN** o sistema rejeita a autenticação com mensagem de credenciais inválidas

#### Scenario: Login com Xano Indisponível
- **WHEN** o usuário tenta realizar o login e o serviço Xano não está acessível
- **THEN** o sistema exibe uma mensagem de falha de conexão com o servidor e não emite um mock JWT
