## ADDED Requirements

### Requirement: Isolamento de Dados e Prestador Único Ativo
O sistema DEVE manter exclusivamente o usuário prestador Hector Barros (id 15) como usuário pré-cadastrado no banco de dados Xano. Todos os demais registros de teste obsoletos, contas sem credenciais ou usuários desconectados DEVEM ser expurgados garantindo a integridade relacional entre as tabelas `user`, `cliente` e `event_log`. Novas contas de clientes DEVEM ser criadas a partir do zero via formulário de cadastro com senha em hash nativo.

#### Scenario: Login Exclusivo do Prestador Hector
- **WHEN** o prestador Hector realiza login com suas credenciais válidas (`hector.barros@aluno.impacta.edu.br`)
- **THEN** o sistema autentica com sucesso contra o Xano, emite o `authToken` e identifica o perfil como `prestador` sem depender de mocks em memória

#### Scenario: Base Limpa para Cadastro de Novo Cliente
- **WHEN** um novo cliente realiza cadastro inicial na plataforma limpa
- **THEN** o registro é criado no Xano com role `cliente`, senha criptografada em hash seguro e perfil estendido criado sem conflito com dados legados
