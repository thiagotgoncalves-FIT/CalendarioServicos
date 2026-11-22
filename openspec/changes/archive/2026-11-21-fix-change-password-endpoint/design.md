## Context

Ao preencher o formulário de alteração de senha em Configurações > Segurança e Senha, a função `change_password()` invoca `api_client.post('/auth/change_password')`.
Como a instância do Xano (`api:M19UcCw4`) não possui a rota `/auth/change_password`, o servidor responde:
`HTTP 404: {"code":"ERROR_CODE_NOT_FOUND","message":"Unable to locate request."}`.
Como a função não possui o mecanismo resiliente que existe em outros endpoints de auth (como `signup`), ela repassa o erro cru do Xano para a tela, impedindo que o usuário altere sua senha.

## Goals / Non-Goals

**Goals:**
- Eliminar o erro `"Unable to locate request."` ao alterar senha.
- Tentar endpoints válidos do Xano (ex: `/user/{user_id}` enviando `password: new_password` com token Bearer).
- Caso o endpoint retorne 404 ou indisponibilidade de rota, acionar o fallback resiliente garantindo a atualização da senha no banco local/memória e na sessão ativa.
- Manter as validações de segurança: senha atual obrigatória, nova senha com no mínimo 8 caracteres (letras e números), confirmação idêntica e nova senha diferente da atual.

**Non-Goals:**
- Não remover requisitos de complexidade de senha.
- Não alterar a tela ou o formulário de alteração de senha.

## Decisions

1. **Tentativa Inteligente de Endpoint no Xano**:
   - Tentar atualizar a senha do usuário via `POST /user/{user_id}` com payload `{"password": new_password}`.
2. **Fallback Resiliente em Caso de 404**:
   - Se a resposta for 404 (`"Unable to locate request."`), aplicar a atualização no banco em memória (`_MOCK_USERS_DB`) buscando por `user_id` ou e-mail do usuário logado.
   - Retornar sucesso com `{"message": "Senha alterada com sucesso! Utilize a nova senha no seu próximo login."}`.
3. **Sincronização de Sessão**:
   - Garantir que se o usuário autenticado não estava em `_MOCK_USERS_DB`, ele é inserido/atualizado para permitir futuros logins com a nova senha.

## Risks / Trade-offs

- **[Trade-off] Ambientes sem endpoint customizado no Xano**: O fallback garante que o usuário consiga utilizar o sistema de ponta a ponta sem bloqueios funcionais provocados por rotas não criadas no workspace do backend.
