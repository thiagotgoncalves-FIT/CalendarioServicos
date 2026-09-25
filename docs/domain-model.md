# Modelo de Domínio — AgendAí

Este documento define os conceitos fundamentais do domínio da plataforma **AgendAí**, suas entidades, responsabilidades, atributos, relacionamentos e regras de negócio essenciais. Ele serve como alinhamento conceitual obrigatório para o design de tabelas no **Xano** e interfaces no **Streamlit**.

---

## 1. Diagrama de Relacionamento Conceitual

```text
       ┌──────────────────────┐
       │       Usuario        │
       │ (Prestador / Cliente)│
       └──────────┬───────────┘
                  │
        ┌─────────┴──────────────────────┐
        │ 1:N                            │ 1:N
        ▼                                ▼
┌────────────────┐              ┌────────────────┐
│    Servico     │              │ Disponibilidade│
│  (do Prestador)│              │  (Dias / Horas)│
└───────┬────────┘              └────────────────┘
        │
        │ 1:N
        ▼
┌────────────────┐
│  Agendamento   │◀───────────── (Cliente: Usuario)
│ (Status/Datas) │
└───────┬────────┘
        │
        │ 1:N
        ▼
┌────────────────┐
│   Historico/   │
│   Auditoria    │
└────────────────┘
```

---

## 2. Entidades Principais

### 2.1 Usuário (`Usuario`)
Representa tanto o prestador de serviço autônomo quanto o cliente que agenda os serviços.

- **Responsabilidade**: Gerenciamento de credenciais, perfil de acesso e informações de contato.
- **Campos Principais**:
  - `id`: Identificador único (Primary Key no Xano).
  - `nome`: Nome completo ou nome fantasia do profissional.
  - `email`: Endereço de e-mail (usado para autenticação; único no sistema).
  - `senha`: Hash criptográfico da senha (gerenciado com segurança no Xano).
  - `telefone`: WhatsApp ou telefone para contato/notificações.
  - `role`: Perfil de acesso (`prestador`, `cliente` ou `admin`).
  - `bio_descricao`: Breve descrição do perfil ou especialidade (relevante para prestadores).
  - `criado_em`: Timestamp de criação do registro.
- **Regras Estruturais**:
  - O e-mail deve ser único no sistema.
  - O perfil define as telas e ações permitidas (um `cliente` não cadastra serviços de outros; um `prestador` gerencia sua própria agenda e serviços).

---

### 2.2 Serviço (`Servico`)
Representa cada tipo de atendimento ou serviço oferecido por um prestador independente.

- **Responsabilidade**: Definir o catálogo comercial, precificação e o tempo de execução do serviço.
- **Campos Principais**:
  - `id`: Identificador único.
  - `prestador_id`: Chave estrangeira referenciando o `Usuario` prestador dono do serviço.
  - `titulo`: Nome do serviço (ex.: "Corte Degradê", "Treino Funcional 1h", "Manicure Tradicional").
  - `descricao`: Detalhes sobre o que está incluso no serviço.
  - `preco`: Valor cobrado em Reais (BRL, numérico decimal).
  - `duracao_minutos`: Duração estimada em minutos (ex.: 30, 45, 60, 90). Essencial para cálculo de slots de agenda.
  - `ativo`: Booleano (indica se o serviço está visível para novos agendamentos).
- **Relacionamentos**:
  - Pertence a um `Usuario` (`prestador_id`).
  - Pode ter múltiplos `Agendamento` associados.
- **Regras Estruturais**:
  - Apenas o prestador proprietário do serviço pode alterá-lo ou inativá-lo.
  - `duracao_minutos` deve ser maior que zero (recomendado em múltiplos de 15 ou 30 minutos).

---

### 2.3 Disponibilidade / Horário de Trabalho (`Disponibilidade`)
Define a grade semanal de expediente e atendimento configurada pelo prestador.

- **Responsabilidade**: Parametrizar em quais dias e horários o prestador aceita reservas.
- **Campos Principais**:
  - `id`: Identificador único.
  - `prestador_id`: Chave estrangeira referenciando o `Usuario` prestador.
  - `dia_semana`: Número ou identificador do dia (0 = Domingo, 1 = Segunda, ..., 6 = Sábado).
  - `hora_inicio`: Horário inicial de atendimento (ex.: `09:00`).
  - `hora_fim`: Horário de término do expediente (ex.: `18:00`).
  - `intervalo_inicio`: Início da pausa/almoço (opcional, ex.: `12:00`).
  - `intervalo_fim`: Fim da pausa/almoço (opcional, ex.: `13:00`).
  - `ativo`: Booleano indicando se o dia está habilitado.
- **Regras Estruturais**:
  - `hora_inicio` deve ser estritamente anterior a `hora_fim`.
  - Intervalos de pausa devem estar contidos dentro do período de atendimento.

---

### 2.4 Agendamento (`Agendamento`)
Representa a reserva de um serviço em uma data e horário específicos entre um cliente e um prestador.

- **Responsabilidade**: Orquestrar a reserva, controle de conflitos de horário e acompanhamento do ciclo de vida do atendimento.
- **Campos Principais**:
  - `id`: Identificador único.
  - `prestador_id`: Chave estrangeira para o `Usuario` prestador.
  - `cliente_id`: Chave estrangeira para o `Usuario` cliente solicitante.
  - `servico_id`: Chave estrangeira para o `Servico` agendado.
  - `data_hora_inicio`: Timestamp com a data e hora de início do atendimento.
  - `data_hora_fim`: Timestamp com a data e hora de término (calculada a partir de `data_hora_inicio` + `duracao_minutos` do serviço).
  - `valor_cobrado`: Snapshot do preço do serviço no momento do agendamento.
  - `status`: Estado atual do agendamento (`pendente`, `confirmado`, `concluido`, `cancelado`).
  - `observacoes`: Informações adicionais enviadas pelo cliente ou pelo prestador.
  - `criado_em`: Data e hora de criação do agendamento.
- **Relacionamentos**:
  - Pertence a um `Usuario` prestador e a um `Usuario` cliente.
  - Referencia um `Servico`.
- **Regras Estruturais e de Negócio**:
  - **Prevenção de Duplo Agendamento (Double Booking)**: Não é permitido criar ou confirmar um agendamento cujo intervalo `[data_hora_inicio, data_hora_fim]` colida com outro agendamento ativo (`pendente` ou `confirmado`) do mesmo prestador.
  - **Bloqueio de Passado**: Agendamentos só podem ser marcados para datas/horários futuros.
  - **Respeito à Grade**: O horário deve estar dentro do expediente ativo da `Disponibilidade` do prestador para aquele dia da semana.
  - **Ciclo de Estados**:
    - `pendente` ➔ Pode ir para `confirmado` ou `cancelado`.
    - `confirmado` ➔ Pode ir para `concluido` ou `cancelado`.
    - `concluido` / `cancelado` ➔ Estados terminais.

---

### 2.5 Registro de Atividade / Auditoria (`RegistroAtividade`)
Registra transições e operações relevantes no sistema para fins de auditoria e notificações.

- **Responsabilidade**: Histórico de ações e transparência.
- **Campos Principais**:
  - `id`: Identificador único.
  - `agendamento_id`: Referência opcional ao agendamento afetado.
  - `usuario_id`: Usuário que disparou a ação.
  - `tipo_evento`: Código do evento (ex.: `AGENDAMENTO_CRIADO`, `AGENDAMENTO_CONFIRMADO`, `AGENDAMENTO_CANCELADO`).
  - `descricao`: Mensagem descritiva do evento.
  - `criado_em`: Timestamp do registro.

---

## 3. Diretrizes de Evolução e Persistência
1. As tabelas correspondentes serão criadas e mantidas no **Xano**.
2. Cada funcionalidade será proposta via OpenSpec (`/opsx-propose`), garantindo validação de payloads REST antes do desenvolvimento no frontend Streamlit.
3. Regras de validação de horário e conflitos serão implementadas com lógica de backend no Xano para garantir robustez e segurança.
