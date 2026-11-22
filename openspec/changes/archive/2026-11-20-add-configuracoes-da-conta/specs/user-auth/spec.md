## ADDED Requirements

### Requirement: Navegação para Tela de Configurações da Conta
O sistema SHALL disponibilizar no card de perfil ativo da barra lateral um ícone de engrenagem clicável com acessibilidade ("Configurações"), dica flutuante (tooltip) e indicação de foco. Ao ser acionado por qualquer usuário autenticado (perfis "prestador" ou "cliente"), o sistema SHALL abrir uma tela dedicada de Configurações da Conta, separada dos painéis operacionais, contendo um botão "Voltar" que restaura o painel anterior sem perda de sessão.

#### Scenario: Acesso à tela de configurações a partir da barra lateral
- **WHEN** o usuário autenticado clica no ícone de engrenagem na barra lateral
- **THEN** o sistema SHALL renderizar a tela de Configurações da Conta para o respectivo usuário, exibindo o botão "Voltar" e as seções de foto, dados pessoais, aparência e segurança

#### Scenario: Retorno à tela principal via botão Voltar
- **WHEN** o usuário clica no botão "Voltar" na tela de Configurações
- **THEN** o sistema SHALL retornar imediatamente ao painel principal correspondente ao perfil do usuário ativo

### Requirement: Edição de Dados Pessoais e Foto de Perfil
O sistema SHALL permitir que o usuário autenticado edite seu nome (campo obrigatório) e seu telefone (com máscara brasileira DDD + número e normalização antes da persistência). O campo de e-mail SHALL ser exibido como somente leitura. O sistema SHALL permitir envio de foto de perfil (JPG, PNG ou WebP com limite máximo de 2 MB) com recorte circular e pré-visualização antes de salvar, bem como a remoção da foto e restauração automática das iniciais nominais. Ao salvar, as alterações SHALL ser refletidas instantaneamente na barra lateral e nas saudações da interface.

#### Scenario: Atualização de nome e telefone com sucesso
- **WHEN** o usuário altera seu nome e informa um telefone válido com DDD e clica em "Salvar alterações"
- **THEN** o sistema SHALL atualizar os dados no perfil do usuário, exibir mensagem de sucesso em pt-BR e atualizar imediatamente o nome exibido no card da barra lateral e na saudação da página

#### Scenario: Envio de foto de perfil com prévia e persistência
- **WHEN** o usuário faz o upload de uma imagem válida (JPG, PNG ou WebP) de até 2 MB
- **THEN** o sistema SHALL exibir prévia circular recortada e, após confirmação, salvar o arquivo na pasta de avatares e atualizar o avatar em todos os pontos da interface

#### Scenario: Remoção de foto e restauração de iniciais
- **WHEN** o usuário que possui foto de perfil clica em "Remover foto"
- **THEN** o sistema SHALL excluir a foto associada e restabelecer imediatamente a exibição do avatar com as iniciais do nome

#### Scenario: Rejeição de arquivo de foto inválido ou excedente a 2 MB
- **WHEN** o usuário tenta enviar um arquivo com extensão não permitida ou com tamanho superior a 2 MB
- **THEN** o sistema SHALL impedir o upload e exibir mensagem explicativa orientando o envio de imagens JPG, PNG ou WebP de até 2 MB

### Requirement: Preferência e Persistência de Tema da Interface
O sistema SHALL disponibilizar opções de tema "Claro" e "Escuro" na seção de Aparência. A escolha do usuário SHALL ser persistida em sua conta e aplicada dinamicamente a todas as telas, cards, abas, tabelas, modais e formulários com garantia de contraste e legibilidade, sendo mantida entre novos logins e sessões em qualquer dispositivo.

#### Scenario: Alternância e persistência de tema
- **WHEN** o usuário seleciona o tema "Escuro" (ou "Claro") e confirma a preferência
- **THEN** o sistema SHALL atualizar os tokens visuais da aplicação imediatamente e persistir a configuração no perfil do usuário para os próximos acessos

#### Scenario: Garantia de contraste e legibilidade nos componentes
- **WHEN** o tema selecionado for o "Escuro"
- **THEN** o sistema SHALL assegurar que todos os fundos (incluindo barra lateral, contêineres de formulário, cards e campos de entrada) adotem tons escuros profundos (#0B0F19, #0F172A e #1E293B) sem áreas residuais brancas, e que todas as letras, rótulos e títulos adotem cor branca (#F8FAFC) com alta legibilidade e contraste

### Requirement: Alteração Segura de Senha
O sistema SHALL disponibilizar na seção de Segurança da tela de configurações a funcionalidade de alteração de senha da conta, exigindo obrigatoriamente a senha atual como mecanismo de autenticação. A nova senha SHALL atender aos requisitos mínimos de segurança (mínimo de 8 caracteres alfanuméricos contendo ao menos uma letra e um número). O sistema SHALL impedir a alteração caso a senha atual esteja incorreta, a nova senha seja fraca ou haja divergência na confirmação.

#### Scenario: Alteração de senha com credenciais válidas
- **WHEN** o usuário informa a senha atual correta e uma nova senha válida com sua confirmação idêntica
- **THEN** o sistema SHALL atualizar a credencial com hash seguro e exibir feedback de confirmação em pt-BR sem expor dados sensíveis

#### Scenario: Tentativa de alteração com senha atual incorreta
- **WHEN** o usuário informa uma senha atual divergente da cadastrada
- **THEN** o sistema SHALL rejeitar a alteração com mensagem de erro clara informando que a senha atual está incorreta

#### Scenario: Tentativa de alteração com nova senha fraca
- **WHEN** o usuário tenta cadastrar uma nova senha com menos de 8 caracteres ou sem letras e dígitos
- **THEN** o sistema SHALL bloquear a operação e destacar os critérios de força exigidos

