## 1. Preparação do Xano (CLI)

- [x] 1.1 Confirmar estado atual do workspace com `xano workspace pull -w 147997 -b v1` e verificar que os stacks dos 3 endpoints ainda estão vazios nos arquivos `.xs` baixados.
- [x] 1.2 Editar `table/user.xs` alterando `enum role` de `["admin", "member"]` para `["prestador", "cliente"]` e verificar que o arquivo está sintaticamente correto.

## 2. Implementação dos Endpoints no Xano (XanoScript)

- [x] 2.1 Implementar o Function Stack de `signup_POST.xs`: inputs (`name`, `email`, `password`, `phone`, `role`), verificar email duplicado (query + precondition), `createRecord` na tabela `user`, `getAuthToken`, response com `authToken` + `user` (sem campo `password`). Verificar: arquivo `.xs` salvo sem erros de sintaxe.
- [x] 2.2 Implementar o Function Stack de `login_POST.xs`: inputs (`email`, `password`), `getAuthToken` com `checkPassword` (mecanismo nativo Xano), response com `authToken` + `user`. Verificar: arquivo `.xs` salvo sem erros de sintaxe.
- [x] 2.3 Implementar o Function Stack de `me_GET.xs`: autenticação obrigatória (`$auth` middleware), response com dados de `$auth.user`. Verificar: arquivo `.xs` salvo sem erros de sintaxe.
- [x] 2.4 Executar `xano workspace push -w 147997 -b v1` e verificar que o push é concluído sem erros.

## 3. Validação dos Endpoints no Xano

- [x] 3.1 Testar `POST /auth/signup` via Python com payload `{name, email, password (8+ chars, 1 letra, 1 dígito), phone, role}` e verificar que o retorno contém `authToken` e `user.id` (não-null).
- [x] 3.2 Testar `POST /auth/login` com as mesmas credenciais recém-criadas e verificar que retorna `authToken` válido.
- [x] 3.3 Testar `GET /auth/me` com o token obtido no login e verificar que retorna os dados do usuário sem o campo `password`.
- [x] 3.4 Testar signup com e-mail duplicado e verificar que retorna erro (não `null`).
- [x] 3.5 Testar login com senha errada e verificar que retorna erro (não `null`).

## 4. Ajustes no Backend Python

- [x] 4.1 Atualizar `auth_service.py`: remover a condição de fallback para `200 null` (`data is None`) quando `status_code == 200`; manter fallback apenas para erros de infraestrutura (`status_code in (500, 502, 503, 504)` e exceção de rede/timeout).
- [x] 4.2 Atualizar validação de senha em `auth_service.py`: alterar o mínimo de 6 para 8 caracteres e adicionar validação de ao menos 1 letra e 1 dígito (alinhado com o Xano).
- [x] 4.3 Atualizar `api_client.py` se necessário: garantir que `status_code` seja retornado corretamente para respostas com body vazio ou `null`.
- [x] 4.4 Verificar `app.py` ou formulário de signup no Streamlit: garantir que a mensagem de validação de senha mínima exibida ao usuário mencione os novos critérios (8 chars, 1 letra, 1 dígito).

## 5. Validação End-to-End

- [x] 5.1 Com o app Streamlit rodando, realizar signup de novo usuário com dados válidos e verificar que a conta é criada no Xano (sem fallback local).
- [x] 5.2 Realizar login com o usuário recém-criado e verificar que a sessão é estabelecida com token JWT real (não `jwt_session_*` mock).
- [x] 5.3 Verificar que `st.session_state` armazena o token JWT real e que a navegação entre páginas mantém a sessão.
- [x] 5.4 Verificar nos logs ou no dashboard do Xano que o registro do usuário existe na tabela `user` com `password` como hash (não texto puro).
