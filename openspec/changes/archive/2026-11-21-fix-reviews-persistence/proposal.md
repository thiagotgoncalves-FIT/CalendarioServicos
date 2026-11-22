# Proposta: Persistência Permanente de Avaliações e Status de Atendimentos Avaliados

## 1. Contexto e Diagnóstico

Ao submeter uma avaliação pós-atendimento, o usuário relatou dois sintomas principais:
1. **A avaliação recém-enviada não aparece em "Detalhes do Serviço"**: Ao abrir a modal de detalhes do serviço ou recarregar a página, a avaliação não é exibida e as métricas do serviço não refletem a nota.
2. **Re-solicitação de avaliação ao logar novamente**: Mesmo tendo acabado de avaliar o atendimento, ao realizar novo login ou recarregar o app, a janela modal de avaliação reaparece para o mesmo atendimento já avaliado.

### Causa Raiz
- No módulo `services/review_service.py`, quando a gravação remota (Xano) não está disponível ou retorna erro, o sistema salva as avaliações exclusivamente na variável em memória `MOCK_REVIEWS: List[Dict]`.
- No módulo `services/appointment_service.py`, `mark_appointment_reviewed()` apenas marca o status em memória (`app["avaliado"] = True`) na lista volátil `MOCK_APPOINTMENTS`.
- No arquivo `app.py`, o loop de verificação de atendimentos concluídos (`apps_pendentes_avaliacao`) chama `review_service.is_appointment_reviewed(a.get("id"))`. Como a lista `MOCK_REVIEWS` é resetada ao reiniciar o Streamlit e a chamada `api_client.get(f"reviews/appointment/{agendamento_id_str}")` não encontra o registro no backend, a verificação retorna `False`, reabrindo o modal na próxima sessão de login.
- Como o Streamlit reinicia o contexto de execução ou recarrega instâncias, todos os dados em memória RAM são perdidos caso não estejam gravados de forma durável em disco (em pasta local segura como `uploads/reviews.json` e `uploads/reviewed_appointments.json`), padrão já consolidado no projeto para avatares e credenciais em `uploads/`.

## 2. Escopo da Mudança

1. **Persistência durável em arquivo (`uploads/reviews.json`)**:
   - Criar camada de leitura e escrita atômica/resiliente em arquivo JSON em disco.
   - Toda nova avaliação inserida via `submit_review` deve ser gravada imediatamente no arquivo JSON em disco, além do cache de memória.
   - `get_reviews` e `get_metrics` devem ler e mesclar os dados persistidos garantindo que qualquer avaliação recém-submetida seja apresentada imediatamente e persista entre reinicializações do app.

2. **Persistência do status de avaliação por agendamento (`uploads/reviewed_appointments.json`)**:
   - Salvar o conjunto de IDs de agendamentos avaliados em arquivo persistente (`uploads/reviewed_appointments.json`).
   - Atualizar `is_appointment_reviewed` e `mark_appointment_reviewed` para consultar e atualizar a lista persistida em disco.
   - Garantir que tanto para agendamentos do backend quanto do mock, uma vez avaliado, o agendamento seja reconhecido permanentemente como avaliado, impedindo a reabertura do modal no login.

3. **Integração com "Detalhes do Serviço" em `app.py`**:
   - Assegurar que `show_service_details_dialog` e a listagem de avaliações consultem o `review_service` atualizado com leitura do arquivo JSON em disco.

4. **Validação Automatizada**:
   - Expandir a suíte `test_review_system.py` para testar persistência em disco, integridade entre reinicializações simuladas e bloqueio definitivo de reavaliação pós-login.
