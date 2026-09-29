## Context

Com base no `docs/domain-model.md` e `docs/project-overview.md`, as entidades centrais do prestador para viabilizar reservas são `Servico` e `Disponibilidade`. Esta mudança implementa a persistência, os endpoints REST e as interfaces Streamlit correspondentes.

## Goals / Non-Goals

**Goals:**
- Definir modelagem física no Xano para as tabelas `servico` e `disponibilidade`.
- Criar contratos REST claros:
  - `GET /services` (com filtro por `prestador_id`)
  - `POST /services` (criação com validação de `prestador_id` extraído do token JWT)
  - `PUT /services/{id}` (edição ou alteração de status ativo)
  - `GET /availability` (consulta da grade do prestador)
  - `POST /availability` (atualização da grade semanal do prestador)
- Implementar módulos de integração frontend em `services/catalog_service.py` e `services/availability_service.py` com fallback em memória para desenvolvimento ágil.
- Aprimorar o painel do prestador em `app.py` com abas visuais ricas para catálogo e horários.

**Non-Goals:**
- Definição de exceções pontuais na agenda (ex.: feriado de Natal, férias de 15 dias).
- Alocação de recursos físicos (salas, cadeiras específicas).
- Verificação cruzada com agendamentos existentes (será o foco da Fatia 3 - Motor de Agendamento).

## Decisions

### 1. Modelagem Física no Xano

#### Tabela `servico`
- `id`: integer, autoincrement, primary key
- `prestador_id`: integer, foreign key -> `user.id`
- `titulo`: text, not null
- `descricao`: text, nullable
- `preco`: decimal (ex: 45.00), not null
- `duracao_minutos`: integer (ex: 30, 45, 60), not null
- `ativo`: boolean, default `true`
- `created_at`: timestamp

#### Tabela `disponibilidade`
- `id`: integer, autoincrement, primary key
- `prestador_id`: integer, foreign key -> `user.id`
- `dia_semana`: integer (0 = Domingo, 1 = Segunda, ..., 6 = Sábado)
- `hora_inicio`: time / text ("09:00")
- `hora_fim`: time / text ("18:00")
- `intervalo_inicio`: time / text ("12:00", nullable)
- `intervalo_fim`: time / text ("13:00", nullable)
- `ativo`: boolean, default `true`

### 2. Contratos REST de Serviços

- `GET /services?prestador_id={id}`: Retorna a lista de serviços do prestador.
- `POST /services`: Payload com `titulo`, `descricao`, `preco`, `duracao_minutos`. O `prestador_id` é herdado do token de autenticação JWT.
- `PUT /services/{id}`: Payload com campos atualizados (ex: toggle de `ativo`).

### 3. Contratos REST de Disponibilidade

- `GET /availability?prestador_id={id}`: Retorna a lista com a configuração dos 7 dias da semana do prestador.
- `POST /availability`: Payload com lista de configurações de dias para atualização em lote.

### 4. Camada de Integração Frontend (`services/`)
- `services/catalog_service.py`: gerencia catálogo com funções `get_services(prestador_id, token)`, `create_service(...)`, `toggle_service_status(...)`.
- `services/availability_service.py`: gerencia horários com funções `get_availability(prestador_id, token)`, `save_availability(prestador_id, schedule_data, token)`.
- Ambas incluem dados simulados padrão para prestadores pré-cadastrados (ex.: Carlos Barbeiro com serviços de "Corte Degradê" e "Barba Terapia").

### 5. Arquitetura de Interface Streamlit
- Substituição do painel estático atual do prestador por sistema de abas intuitivas:
  - 📊 **Métricas & Resumo**
  - ✂️ **Catálogo de Serviços** (criação rápida, visualização em cards modernos e métricas de ticket médio)
  - 🕒 **Grade de Atendimento** (seleção de dias e ajuste de horários com feedback em tempo real)
- Na Área do Cliente, inclusão de visualização do catálogo do prestador selecionado para demonstrar o valor gerado de ponta a ponta.

## Risks / Trade-offs

- **[Fuso Horário e Formato de Horário]** → Padronizado no formato `HH:MM` em texto de 24 horas no frontend para evitar ambiguidades com fusos locais.
- **[Persistência Offline]** → O fallback local garante que mesmo sem instanciar o Xano neste exato momento, o usuário e a banca do professor conseguem rodar e testar imediatamente no Streamlit.
