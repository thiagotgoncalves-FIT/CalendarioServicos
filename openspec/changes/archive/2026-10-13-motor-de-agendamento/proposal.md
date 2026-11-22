## Why

Atualmente, o AgendAí já possui cadastro/login com separação de perfis (Prestador vs Cliente), catálogo de serviços e configuração de grade semanal de disponibilidade. No entanto, o cliente ainda não consegue agendar serviços pelo catálogo (o botão "Agendar Horário" está desativado) e o prestador não possui visualização nem controle de status dos agendamentos recebidos.

Esta mudança introduz o motor de agendamento central da plataforma (Fatia 3 / C3), permitindo o cálculo dinâmico de horários livres, prevenção de conflitos de horário (anti-double-booking), criação de reservas pelo cliente e gerenciamento de status pelo prestador.

## What Changes

- **Motor de cálculo de slots livres**: Algoritmo com passo de 30 minutos que cruza a grade semanal do prestador (expediente e almoço/pausa) com a duração do serviço escolhido e os agendamentos já confirmados/pendentes no dia.
- **Validação de agendamentos no passado**: Bloqueio de seleção de horários anteriores ao horário atual para a data de hoje.
- **Camada de Serviço de Agendamentos (`services/appointment_service.py`)**: Implementação de cliente de API HTTP para endpoints de agendamento (`/appointments`), integrado com fallback resiliente em memória para execução e testes autônomos.
- **Interface do Cliente (`app.py`)**: Ativação do fluxo de agendamento a partir do catálogo, com seleção de data (`st.date_input`), chips/seletor de slots livres disponíveis, confirmação imediata e aba/seção "Meus Agendamentos" com cancelamento.
- **Interface do Prestador (`app.py`)**: Nova aba/seção de "Agenda e Atendimentos", exibindo lista de agendamentos com filtros de data/status e botões de ação rápida (Confirmar, Concluir, Cancelar), além da atualização das métricas do painel resumo.

## Capabilities

### New Capabilities
- `appointment-engine`: Motor de cálculo de horários livres, criação de reservas com prevenção de double booking e controle de ciclo de vida/status do agendamento.

### Modified Capabilities
<!-- Nenhuma especificação existente teve seus requisitos alterados. -->

## Impact

- **Código Frontend**: Modificação de `app.py` para enriquecer as visões de Prestador (nova aba de Agenda) e Cliente (ativação do fluxo de agendamento e listagem de histórico).
- **Código de Serviços**: Criação de `services/appointment_service.py` consumindo `services/api_client.py`.
- **APIs & Backend**: Novos endpoints REST (`GET /appointments`, `POST /appointments`, `POST /appointments/{id}/status`) com suporte a mock resiliente.
