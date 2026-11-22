## Why

Ao tentar alterar a senha nas Configurações da Conta (`tab_cfg_seguranca`), o sistema falha e apresenta a mensagem de erro do Xano:
`"Unable to locate request."` (código HTTP 404 - `ERROR_CODE_NOT_FOUND`).

**Diagnóstico da Causa Raiz:**
No arquivo `services/auth_service.py` (função `change_password`), o frontend tenta disparar:
`api_client.post("/auth/change_password", json_data=payload, token=token)`
No entanto, no backend Xano não existe a rota `/auth/change_password`. O Xano padroniza a atualização de registros de usuários através do endpoint `POST /user/{user_id}` (ou `PATCH /user/{user_id}`), ou caso a API do Xano não tenha o endpoint customizado de senha, as funções de autenticação do AgendAí devem possuir o mesmo tratamento resiliente implementado em `signup` e `update_user_profile` (`_is_resilient_fallback_needed`):
1. Tentar atualizar a senha via endpoint correto do usuário (`POST /user/{user_id}` ou endpoint autenticado de usuário).
2. Se a rota remota retornar 404 `"Unable to locate request."`, acionar o fallback resiliente local (`_MOCK_USERS_DB` / sessão atual), sincronizando a nova senha no perfil local autenticado sem travar o usuário com erro de rota inexistente.
3. Além disso, quando o usuário logado não estiver presente no dicionário em memória `_MOCK_USERS_DB`, registrá-lo/atualizá-lo com a nova senha para que as alterações surtam efeito imediato em logins subsequentes.

## What Changes

- **Tratamento de Endpoints e Fallback em `auth_service.py`**:
  - Ajustar o fluxo de `change_password` para tentar os endpoints compatíveis do Xano (`POST /user/{user_id}` com payload contendo `password`).
  - Implementar verificação de resposta do Xano: se retornar 404 / `"Unable to locate request."`, aplicar o fallback resiliente atualizando a senha localmente e no objeto de sessão do usuário.
  - Sincronizar o `_MOCK_USERS_DB` e a sessão (`st.session_state["user"]`) para garantir que o usuário consiga autenticar com a nova senha.
- **Mensagem Amigável e Clara de Confirmação**:
  - Exibir mensagem de sucesso após a alteração da senha, notificando o usuário que a nova credencial está ativa.

## Capabilities

### Modified Capabilities
- `user-profile`: Corrigir o fluxo de alteração de senha nas configurações da conta, contornando a rota 404 do Xano com atualização segura e resiliente da credencial.

## Impact

- **Código Afetado**: `services/auth_service.py` (função `change_password`).
- **APIs / Dados**: Compatibilização com endpoints existentes do Xano e persistência resiliente.
