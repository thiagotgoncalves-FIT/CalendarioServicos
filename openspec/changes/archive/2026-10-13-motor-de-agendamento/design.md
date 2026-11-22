## Context

O AgendAí conta com módulos de autenticação, catálogo de serviços e grade semanal de atendimento com suporte a Dark Theme nativo no Streamlit. Para viabilizar a marcação de horários de ponta a ponta, é necessário acoplar a grade semanal do prestador aos agendamentos reais/mockados através de um motor que computa janelas de tempo disponíveis.

## Goals / Non-Goals

**Goals:**
- Implementar algoritmo determinístico de geração de slots livres a cada 30 minutos, respeitando pausas, fim de expediente e agendamentos existentes.
- Criar a camada de serviço `appointment_service.py` encapsulando as chamadas HTTP para o backend Xano e provendo fallback em memória resiliente.
- Habilitar no `app.py` a seleção de data e horário pelo cliente e a listagem/gestão da agenda pelo prestador.

**Non-Goals:**
- Integração com gateways de pagamento ou cobrança de adiantamento (escopo de fatia futura).
- Envio de notificações push ou WhatsApp em tempo real (escopo da Fatia de Comunicação).
- Sincronização externa com Google Calendar ou Outlook.

## Decisions

### Decisão 1: Geração de Slots com Passo Fixo de 30 Minutos (Modelo A)
- **Escolha**: Amostrar os horários de início candidatos em intervalos regulares de 30 minutos (ex: 09:00, 09:30, 10:00). Para cada horário candidato $T$, o motor verifica se a janela $[T, T + \text{duracao}]$ cabe dentro do expediente do dia, não intercepta o intervalo de almoço e não colide com agendamentos ativos.
- **Alternativas consideradas**: Passo variável baseado exatamente na duração de cada serviço.
- **Motivação**: O passo fixo cria uma grade visual limpa e padronizada em botões/chips no Streamlit, evita que a agenda do prestador fique fragmentada com fatias de 10 ou 15 minutos inutilizáveis e segue o alinhamento definido com o usuário na fase de exploração.

### Decisão 2: Módulo `services/appointment_service.py` com Mock Fallback
- **Escolha**: Criar um módulo dedicado para agendamentos seguindo o mesmo padrão de resiliência de `catalog_service.py` e `auth_service.py`. Tenta realizar chamadas ao endpoint `/appointments` via `api_client.py`, e caso receba 503/404 ou flag de mock, executa a lógica diretamente sobre uma lista `MOCK_APPOINTMENTS` em memória.
- **Alternativas consideradas**: Fazer chamadas diretas na interface `app.py`.
- **Motivação**: Mantém a arquitetura limpa em camadas (Separação de Preocupações / SoC) e garante que os testes automatizados e a validação do protótipo funcionem mesmo sem uma instância ativa do Xano.

### Decisão 3: Confirmação Imediata no Agendamento
- **Escolha**: Ao escolher um slot livre e confirmar, o agendamento é registrado diretamente com o status `confirmado`.
- **Alternativas consideradas**: Fluxo de aprovação manual obrigatória (`pendente` aguardando clique do prestador).
- **Motivação**: Reduz a fricção para o cliente final e atende ao objetivo central de reduzir trocas manuais de mensagens. O prestador mantém a prerrogativa de cancelar ou remarcar o atendimento caso haja imprevisto.

## Risks / Trade-offs

- **[Risco: Persistência volátil em reinicialização do Streamlit no modo Mock]** → *Mitigação*: Inicializar `MOCK_APPOINTMENTS` com sementes demonstrativas e manter estado compartilhado no processo Python durante a sessão de teste.
- **[Risco: Concorrência simultânea no mesmo slot]** → *Mitigação*: O serviço revalida o intervalo no exato momento da chamada de `create_appointment`, impedindo double-booking mesmo se o slot estivesse visível na tela no momento da abertura do formulário.
