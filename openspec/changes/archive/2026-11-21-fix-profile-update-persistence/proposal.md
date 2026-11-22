# Proposta: Persistência Durável de Alterações de Nome e Telefone nas Configurações

## 1. Contexto e Diagnóstico

O usuário relatou: *"meu nome de usuário e telefone não está salvando quando eu troco nas configurações"*.

### Causa Raiz
1. **Volatilidade de Dados Cadastrais**: Em `services/auth_service.py`, a função `update_user_profile()` atualiza os campos `name`, `phone` e `phone_formatted` apenas no dicionário em memória `_MOCK_USERS_DB` e tenta chamar o endpoint remoto `api_client.post(f"/user/{user_id}")`.
2. **Perda nos Logins Subsequentes**:
   - `_MOCK_USERS_DB` é volátil e não é sincronizado com um arquivo em disco.
   - Quando o usuário faz login novamente, o método `login()` consulta `_load_persisted_credentials()`, mas esse arquivo armazena apenas `{"user_id": ..., "password": ...}`, sem os dados atualizados de `name` e `phone`. Como resultado, o login volta a carregar os dados padrão estáticos do mock (ex: "Carlos Barbeiro" ou "Cliente").
   - Se o backend remoto retornar 404 para `/user/{user_id}`, os dados alterados não ficam salvos no Xano.
3. **Falta de Persistência em Disco para Perfis de Usuário**:
   - Da mesma forma que as senhas são persistidas em `uploads/user_credentials.json` e as avaliações em `uploads/reviews.json`, o cadastro completo e atualizado dos usuários (nome, telefone, telefone formatado, e-mail e tema) necessita de persistência durável no diretório `uploads/` (ex: `uploads/user_profiles.json` ou enriquecimento em `uploads/user_credentials.json`).

## 2. Escopo da Mudança

1. **Persistência Durável em Arquivo JSON (`uploads/user_profiles.json`)**:
   - Criar funções `_load_persisted_profiles()` e `_save_persisted_profile(user_id, name, phone, email)` em `services/auth_service.py`.
   - Na inicialização e na autenticação (`login`, `signup`, `get_current_user`), carregar e mesclar os perfis persistidos em disco.
2. **Atualização em `update_user_profile`**:
   - Ao salvar as alterações cadastrais (nome e telefone formatado), salvar imediatamente no arquivo persistente em disco além de atualizar `_MOCK_USERS_DB` e a sessão (`st.session_state["user"]`).
   - Tentar atualizar no backend remoto via `api_client.post(f"/user/{user_id}")` ou `api_client.patch(f"/user/{user_id}")` tratando falhas com resiliência sem perder o dado.
3. **Preservação de Dados no Re-login e Navegação**:
   - Ao realizar novo login com e-mail/senha, carregar o nome e o telefone atualizados do arquivo de perfis persistidos.
   - Garantir que a área do cliente/prestador e a aba de Configurações exibam os dados cadastrais atualizados permanentemente.
4. **Validação e Testes Automatizados**:
   - Adicionar testes em `test_user_settings.py` validando alteração de nome e telefone, persistência durável em disco e integridade após reinicialização completa/re-login.
