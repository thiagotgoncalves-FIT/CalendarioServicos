## Why

Os endpoints `/auth/signup`, `/auth/login` e `/auth/me` existem no API Group `Authentication` do Xano (canonical `M19UcCw4`), porém seus Function Stacks estão completamente vazios — sem inputs, sem lógica e sem resposta. Isso faz com que toda chamada retorne `null` (HTTP 200), ativando sempre o mock fallback local e impedindo que qualquer dado real seja persistido no banco do Xano.

## What Changes

- **`xano/` (Function Stacks via Xano CLI)**: Implementar a lógica completa de `auth/signup`, `auth/login` e `auth/me` nos arquivos `.xs` e fazer `workspace push` para publicar no Xano.
- **`table/user.xs`**: Alterar o `enum role` de `["admin", "member"]` para `["prestador", "cliente"]` para alinhar com o domínio do AgendAí.
- **`services/auth_service.py`**: Remover a condição de fallback para erros gerados pela ausência de lógica nos endpoints (resposta `null` não deve mais acionar resiliência quando o Xano está ativo).
- **`.env.example`**: Documentar as variáveis de ambiente necessárias para integração real.
- **`services/api_client.py`**: Ajustar a validação de senha mínima de 6 para 8 caracteres (exigência do Xano: mínimo 8 chars com 1 letra e 1 dígito).

## Capabilities

### New Capabilities
<!-- Nenhuma nova capability de negócio. A autenticação já está especificada em user-auth. -->

### Modified Capabilities
- `user-auth`: Os requisitos de signup agora incluem persistência real no Xano com senha com hash, validação de email duplicado com erro 409 e geração de JWT authToken.

## Impact

- **Xano (backend)**: 4 arquivos `.xs` alterados e publicados via `xano workspace push`.
- **Backend Python**: `services/auth_service.py`, `services/api_client.py`.
- **Variáveis de ambiente**: `.env` (valor real) e `.env.example` (modelo documentado).
- **Sem impacto de dados**: não há registros existentes na tabela `user` (endpoints estavam vazios, zero cadastros reais).
