# Tarefas: Persistência Durável de Alterações de Perfil

- [x] 1. Implementar armazenamento durável de perfis em `services/auth_service.py` <!-- id: 1-persist-profiles-json -->
  - Criar `_load_persisted_profiles()` e `_save_persisted_profile()` apontando para `uploads/user_profiles.json`.
  - Criar função auxiliar `_enrich_user_from_persisted_profile()`.
  - Atualizar `update_user_profile()` para salvar duravelmente no disco e aceitar parâmetro `email`.
  - Integrar `login()` e `get_current_user()` para enriquecer dados cadastrais com os perfis persistidos.

- [x] 2. Ajustar formulário de dados cadastrais em `app.py` <!-- id: 2-integrate-app-profile-form -->
  - Passar o e-mail do usuário logado na chamada de `auth_service.update_user_profile()`.
  - Garantir atualização imediata de `st.session_state["user"]` e recarregamento sem perdas.

- [x] 3. Expandir suíte de testes e validar conformidade <!-- id: 3-test-and-validate -->
  - Adicionar testes em `test_user_settings.py` para persistência em disco de nome e telefone e verificação pós-reload e pós-login.
  - Executar as suítes de testes automatizados (`test_user_settings.py`, `test_review_system.py`, `test_appointment_engine.py`).
  - Executar `openspec validate fix-profile-update-persistence --strict`.
