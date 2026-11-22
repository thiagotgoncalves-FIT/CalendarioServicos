## 1. Persistência de Credenciais em Disco e Vínculo por E-mail

- [x] 1.1 Em `services/auth_service.py`, implementar salvamento e carregamento de credenciais alteradas em arquivo JSON persistente (`uploads/user_credentials.json`).
- [x] 1.2 Atualizar `change_password` para aceitar `email` do usuário logado e atualizar o registro indexado por e-mail tanto na memória quanto no arquivo persistente.
- [x] 1.3 Atualizar `app.py` na chamada de `change_password()` para enviar `email=user.get("email")`.

## 2. Validação no Fluxo de Login (`login`)

- [x] 2.1 Em `login()`, verificar se existe credencial persistida para o e-mail: se a senha digitada corresponder à nova senha salva, autorizar login imediatamente; se for a senha antiga, bloquear o login.
- [x] 2.2 Garantir que o recarregamento da aplicação mantém a nova senha ativa.

## 3. Testes e Validação

- [x] 3.1 Executar os testes automatizados do projeto (`test_user_settings.py`, `test_appointment_engine.py`).
- [x] 3.2 Validar a especificação estrita do OpenSpec com `openspec validate fix-change-password-endpoint --strict`.
