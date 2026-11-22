# Design: Persistência Durável de Alterações de Perfil de Usuário

## 1. Arquitetura da Solução

O sistema adotará o padrão consolidado do projeto com armazenamento em arquivo JSON no diretório persistente `uploads/user_profiles.json`, garantindo resiliência operacional quando a API remota estiver inacessível ou em modo local.

### 1.1 Arquivo de Armazenamento
- Caminho: `uploads/user_profiles.json`
- Estrutura:
```json
{
  "carlos@barbearia.com": {
    "user_id": 1,
    "name": "Carlos Silva Barbeiro",
    "phone": "11987654321",
    "phone_formatted": "(11) 98765-4321",
    "email": "carlos@barbearia.com",
    "atualizado_em": "2026-11-21 13:10:00"
  }
}
```

## 2. Modificações em Módulos

### 2.1 `services/auth_service.py`
1. **Funções Auxiliares**:
   - `_load_persisted_profiles() -> Dict[str, Dict[str, Any]]`: Carrega o mapa de perfis persistidos por e-mail (chave lowercase).
   - `_save_persisted_profile(email: str, profile_data: Dict[str, Any]) -> None`: Grava atômica e duravelmente os dados cadastrais atualizados no arquivo JSON.
   - `_enrich_user_from_persisted_profile(user_dict: Dict[str, Any]) -> None`: Atualiza os campos `name`, `phone` e `phone_formatted` no dicionário do usuário caso existam registros persistidos para aquele e-mail.
2. **`update_user_profile(user_id, name, phone, token=None, email=None)`**:
   - Valida nome (2 a 100 caracteres) e telefone com DDD (10 ou 11 dígitos).
   - Formata o telefone brasileiro via `format_phone_br`.
   - Grava os dados atualizados em `uploads/user_profiles.json`.
   - Atualiza `_MOCK_USERS_DB`.
   - Envia requisição para a API remota via endpoint `/user/{user_id}` mantendo a camada de resiliência.
   - Retorna os dados atualizados para sincronização imediata na sessão do Streamlit.
3. **`login(email, password)`**:
   - Ao autenticar o usuário (seja via Xano ou modo resiliente), executa `_enrich_user_from_persisted_profile(u_dict)`.
   - Garante que novos logins reflitam imediatamente o nome e o telefone atualizados.
4. **`get_current_user(token)`**:
   - Enriquece o usuário retornado com os dados persistidos em disco.

### 2.2 `app.py`
- Em `form_edit_user_profile`:
  - Passar `email=user.get("email")` para `auth_service.update_user_profile()`.
  - Atualizar `st.session_state["user"]["name"]` e `st.session_state["user"]["phone"]` com os dados confirmados.

## 3. Validação e Testes
- Adicionar testes automatizados em `test_user_settings.py`:
  - Teste de atualização de perfil com validação de persistência em disco.
  - Teste de login subsequente validando que o nome e telefone persistem entre reinicializações do módulo.
