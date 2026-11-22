# Tarefas: Persistência Durável de Avaliações e Bloqueio de Reavaliação

- [x] 1. Implementar armazenamento em disco de avaliações em `services/review_service.py` <!-- id: 1-persist-reviews-json -->
  - Criar funções `_load_persisted_reviews()` e `_save_persisted_reviews()` apontando para `uploads/reviews.json`.
  - Criar funções `_load_reviewed_appointments()` e `_mark_appointment_persisted_reviewed()` apontando para `uploads/reviewed_appointments.json`.
  - Atualizar `submit_review` para salvar no disco imediatamente.
  - Atualizar `get_reviews` e `get_metrics` para ler do disco em modo local/fallback.
  - Atualizar `is_appointment_reviewed` para checar no arquivo de agendamentos avaliados persistidos.

- [x] 2. Integrar persistência no motor de agendamentos em `services/appointment_service.py` <!-- id: 2-integrate-appointment-service -->
  - Atualizar `mark_appointment_reviewed` para invocar a persistência durável no `review_service`.
  - Enriquecer retornos de `get_appointments_by_user` garantindo que o status `avaliado: True` reflita os agendamentos persistidos.

- [x] 3. Ajustar verificação e fechamento de modal em `app.py` <!-- id: 3-adjust-app-dialogs -->
  - Garantir que `show_service_details_dialog` consulte as avaliações persistidas atualizadas.
  - Garantir que `apps_pendentes_avaliacao` filtre adequadamente agendamentos avaliados via checagem persistente, impedindo reabertura no login.

- [x] 4. Expandir suíte de testes automatizados e validar conformidade <!-- id: 4-test-and-validate -->
  - Adicionar testes em `test_review_system.py` cobrindo persistência em disco, integridade entre reinicializações e bloqueio de reavaliação pós-login.
  - Executar todos os testes do projeto (`test_review_system.py`, `test_appointment_engine.py`, `test_user_settings.py`).
  - Executar `openspec validate fix-reviews-persistence --strict`.
