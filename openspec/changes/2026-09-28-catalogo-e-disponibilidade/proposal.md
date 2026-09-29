## Why

Com a autenticação e segregação de perfis (`prestador` vs. `cliente`) consolidadas na Fatia 1, o prestador autônomo necessita agora cadastrar suas ofertas comerciais e definir quando está disponível para atender.

Sem um **catálogo de serviços** padronizado (com título, preço e duração estimada em minutos) e sem a configuração da **grade semanal de horários de atendimento**, é impossível para o cliente visualizar opções de contratação ou para o sistema calcular slots livres sem conflito de agenda nas fatias subsequentes (Motor de Agendamento).

Esta fatia entrega o núcleo de parametrização operacional do prestador:
1. Gestão completa de seus serviços com valores e tempo de execução.
2. Definição personalizada de dias de expediente, horários de início/fim e intervalos de pausa/almoço.

## What Changes

- Modelagem e especificação das entidades `Servico` e `Disponibilidade` no Xano.
- Especificação de contratos REST para criação, listagem, edição e exclusão de serviços (`/services`), vinculados exclusivamente ao prestador autenticado.
- Especificação de contratos REST para leitura e parametrização dos horários semanais de trabalho (`/availability`).
- Implementação da camada de serviço no frontend Streamlit (`services/catalog_service.py` e `services/availability_service.py`) com integração HTTP e dados simulados elegantes para execução local imediata.
- Interface visual no Painel do Prestador em `app.py`:
  - Aba/Seção de **Gestão do Catálogo de Serviços**: formulário para adicionar novos serviços, visualização em cards com preço e duração, e opção de alternar status (ativo/inativo).
  - Aba/Seção de **Grade de Atendimento (Disponibilidade)**: configuração intuitiva dos dias da semana trabalhados, horários de expediente e intervalos de descanso.
- Visualização preliminar do catálogo para o perfil Cliente na Área do Cliente.
- **Fora do escopo desta mudança**: Cálculo dinâmico de conflitos com agendamentos existentes (pertence à Fatia 3 - Motor de Agendamento), bloqueio de feriados ou dias pontuais de férias, e cobrança/pagamento online.

## Capabilities

### New Capabilities
- `service-catalog`: Capacidade do prestador cadastrar, visualizar, editar e gerenciar seus serviços com título, descrição, preço e tempo de duração (minutos).
- `prestador-availability`: Capacidade do prestador configurar e atualizar sua grade semanal de expediente (dias atendidos, horário de entrada, saída e pausas).

### Modified Capabilities
- `user-auth`: O dashboard do prestador e a área do cliente passam a exibir e consumir dados do catálogo e disponibilidade após o login.

## Impact

- **Backend (Xano)**: Criação das tabelas relacionais `servico` e `disponibilidade` com vínculo à chave estrangeira `user_id` / `prestador_id`.
- **Frontend (Streamlit)**: Expansão do Painel do Prestador com abas de navegação dedicadas e exibição de cards de serviços e formulários reativos.
- **Arquitetura**: Isolamento de dados garantindo que um prestador visualize e altere somente seus próprios serviços e horários.
