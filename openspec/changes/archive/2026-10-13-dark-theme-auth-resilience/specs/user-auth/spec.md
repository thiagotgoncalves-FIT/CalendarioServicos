## MODIFIED Requirements

### Requirement: Cadastro de Usuário com Seleção de Perfil
The system SHALL permitir que um novo usuário se cadastre informando nome, e-mail válido, senha segura, telefone e o perfil de acesso desejado (`prestador` ou `cliente`). O sistema SHALL tentar persistir os dados na API do Xano e, caso a API do Xano retorne resposta nula, incompleta ou erro de serviço/conexão, DEVE realizar fallback inteligente para registro e persistência na sessão local, garantindo que o usuário consiga testar e utilizar a plataforma sem bloqueios.

#### Scenario: Cadastro de Prestador de Serviços com Sucesso
- **WHEN** o usuário submete o formulário de cadastro com nome "Carlos Barbeiro", e-mail "carlos@barbearia.com", senha válida, telefone e seleciona o perfil "prestador"
- **THEN** o sistema cria o registro na tabela de usuários do Xano (ou sessão em modo resiliente), gera o hash seguro da senha e retorna confirmação de sucesso com token de autenticação e papel definido como prestador

#### Scenario: Cadastro de Cliente com Sucesso
- **WHEN** o usuário submete o formulário de cadastro com nome "Mariana Silva", e-mail "mariana@email.com", senha válida, telefone e seleciona o perfil "cliente"
- **THEN** o sistema cria o registro com sucesso no Xano (ou sessão em modo resiliente) e atribui o papel de cliente

#### Scenario: Tentativa de Cadastro com E-mail Já Existente
- **WHEN** o usuário tenta cadastrar uma conta com um endereço de e-mail que já está registrado no sistema (Xano ou sessão local)
- **THEN** o sistema rejeita a operação com código de erro 400/409 e exibe uma mensagem clara informando que o e-mail já está em uso

#### Scenario: Tentativa de Cadastro com Campos Obrigatórios Ausentes
- **WHEN** o usuário submete o formulário com campos essenciais em branco (nome, e-mail ou senha)
- **THEN** o sistema impede a submissão e destaca os campos que necessitam de preenchimento

#### Scenario: Tentativa de Cadastro com Xano Indisponível
- **WHEN** o usuário submete o formulário e a API do Xano não responde, retorna erro 503 ou retorna corpo nulo
- **THEN** o sistema ativa o modo de resiliência, conclui o cadastro com persistência na sessão local, emite token de acesso válido e notifica o usuário sobre o modo ativo de forma transparente

---

### Requirement: Autenticação de Usuário e Emissão de Token
The system SHALL autenticar o usuário a partir de suas credenciais (e-mail e senha) e emitir um token JWT para identificação das requisições subsequentes. A autenticação SHALL ser validada contra o backend do Xano prioritariamente, recorrendo à validação contra a base de usuários da sessão caso o Xano retorne corpo nulo ou esteja inacessível.

#### Scenario: Login com Credenciais Válidas
- **WHEN** o usuário insere seu e-mail e senha corretos e clica em "Entrar"
- **THEN** o sistema valida as credenciais no Xano ou na base local, retorna o token de autenticação JWT, os dados do usuário (nome, e-mail, role) e o direciona para a área correspondente ao seu perfil

#### Scenario: Login com Senha Incorreta
- **WHEN** o usuário insere um e-mail cadastrado no Xano ou localmente, mas com a senha incorreta
- **THEN** o sistema rejeita o login com código 401/403 e apresenta mensagem de erro amigável sem expor detalhes internos

#### Scenario: Login com E-mail Inexistente
- **WHEN** o usuário tenta logar com um e-mail não cadastrado na base do Xano nem na sessão local
- **THEN** o sistema rejeita a autenticação com mensagem de credenciais inválidas

#### Scenario: Login com Xano Indisponível
- **WHEN** o usuário tenta realizar o login e o serviço Xano não está acessível ou retorna corpo nulo
- **THEN** o sistema autentica as credenciais contra a base de dados de sessão local de forma resiliente e emite o token de acesso correspondente

## ADDED Requirements

### Requirement: Interface com Dark Theme Profissional
The system SHALL apresentar toda a interface gráfica de autenticação e navegação sob um tema escuro (Dark Theme) profissional, com alto contraste, paleta consistente e componentes estéticos modernos.

#### Scenario: Visualização Inicial da Tela de Autenticação em Tema Escuro
- **WHEN** o usuário acessa a plataforma sem estar autenticado
- **THEN** a tela exibe fundo escuro sofisticado (Slate/Obsidian), cards de formulário estilizados, campos de digitação com alto contraste e botões de ação primária destacados

#### Scenario: Identificação Visual do Perfil no Dark Theme
- **WHEN** o usuário visualiza as opções de perfil na criação de conta ou no sidebar
- **THEN** os perfis "Prestador de Serviços" e "Cliente" são representados com badges e contrastes visuais distintos e legíveis
