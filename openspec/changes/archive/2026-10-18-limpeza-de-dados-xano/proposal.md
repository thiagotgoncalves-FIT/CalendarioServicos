# Proposta: Limpeza de Dados do Banco Xano e Isolamento do Prestador Hector

## Why
O banco de dados no Xano acumulou registros obsoletos de testes, incluindo contas sem credenciais válidas e múltiplos usuários de desenvolvimento. Para validar o fluxo de cadastro e login de clientes a partir do zero com integridade relacional, é necessário realizar uma limpeza segura e controlada, mantendo unicamente o usuário prestador Hector Barros (id 15).

## What Changes
- Exportação e garantia de backup completo de todas as tabelas em pasta local fora do controle de versão (`backups/`).
- Limpeza relacional em ordem correta (filhos antes dos pais):
  - Remoção de registros da tabela `cliente` vinculados a usuários antigos (id 1, user_id 4).
  - Remoção de logs de atividade da tabela `event_log` vinculados a usuários antigos (10 registros).
  - Remoção de todos os usuários da tabela `user`, exceto Hector (id 15, role `prestador`).
  - Preservação estrita das credenciais (hash de senha), perfil e account_id do Hector.
  - Alinhamento da grafia do nome de exibição do Hector para "Hector Barros" caso confirmado pelo usuário.
- Manutenção integral da arquitetura: nenhuma tabela, coluna, índice ou endpoint será alterado ou removido.

## Capabilities

### Modified Capabilities
- `user-auth`: O sistema passa a operar em ambiente limpo onde apenas o prestador Hector Barros está pré-cadastrado no banco, garantindo que novos cadastros de clientes e testes de autenticação operem com integridade relacional estrita.

## Impact
- **Banco de Dados (Xano)**: Remoção de 13 registros de `user`, 1 registro de `cliente` e 10 registros de `event_log`.
- **Frontend (Streamlit)**: O prestador Hector permanece acessível com suas credenciais. A base de clientes fica zerada para permitir novos cadastros do zero.
- **Segurança**: Backup íntegro e isolamento de chaves estrangeiras sem deixar registros órfãos.
