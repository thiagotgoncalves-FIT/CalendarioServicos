## 1. Camada de Serviço e Motor de Agendamento (`services/appointment_service.py`)

- [x] 1.1 Implementar a estrutura de dados de fallback (`MOCK_APPOINTMENTS`) e a função `calculate_available_slots(prestador_id, date_str, duration_minutes, token)` com passo de 30 minutos, filtrando expediente, almoço, agendamentos já marcados e horários no passado para o dia atual. (Verificar executando teste unitário de cálculo de slots para diferentes dias da semana e horários de intervalo).
- [x] 1.2 Implementar as funções `create_appointment(cliente_id, prestador_id, servico_id, data_str, hora_inicio, token)`, `get_appointments_by_user(user_id, role, token)` e `update_appointment_status(appointment_id, new_status, token)` com prevenção atômica de double-booking e integração com `api_client`. (Verificar criando agendamento de teste, validando colisão de horário e checando a atualização de status para 'concluido' e 'cancelado').

## 2. Interface do Cliente: Fluxo de Reserva e Histórico (`app.py`)

- [x] 2.1 Atualizar o catálogo de serviços na visão do cliente em `app.py`, integrando a seleção de data (`st.date_input`) e exibição dinâmica dos slots livres calculados, ativando o botão de confirmação de agendamento com feedback imediato. (Verificar agendando um serviço como cliente e conferindo mensagem de sucesso e bloqueio subsequente do mesmo slot).
- [x] 2.2 Criar a seção "Meus Agendamentos" na visão do cliente em `app.py`, exibindo lista de atendimentos ativos/passados com badges de status e botão para cancelamento de agendamentos futuros. (Verificar cancelando um agendamento na interface do cliente e observando a liberação do slot no catálogo).

## 3. Interface do Prestador: Agenda de Atendimentos e Métricas (`app.py`)

- [x] 3.1 Adicionar a aba "📅 Agenda" no Painel do Prestador em `app.py`, permitindo visualizar os agendamentos recebidos filtrados por data e status, com ações rápidas para "Concluir Atendimento" e "Cancelar". (Verificar autenticando como prestador, visualizando o agendamento criado pelo cliente e alterando seu status para concluído).
- [x] 3.2 Atualizar as métricas do "📊 Resumo" no Painel do Prestador para refletir a contagem real de "Agendamentos Hoje" e receita prevista a partir dos agendamentos confirmados e concluídos. (Verificar que o card métrico 'Agendamentos Hoje' reflete a quantidade correta para a data atual).

## 4. Testes Integrados e Validação

- [x] 4.1 Criar script de teste automatizado `test_appointment_engine.py` validando o fluxo de ponta a ponta: geração de slots livres, prevenção de conflito/double-booking, criação de agendamento e transições de status. (Verificar executando `python test_appointment_engine.py` com 100% de aprovação).
