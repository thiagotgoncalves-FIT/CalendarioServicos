# Proposal: add-avaliacoes-e-redesign-profissional

## Why

A plataforma AgendAí atualmente expõe termos técnicos, jargões acadêmicos e identificadores internos (como referências a "Backend Xano", "Camada de Resiliência", IDs numéricos de banco e dados de depuração) que degradam a experiência do cliente final e transmitem uma percepção de "ferramenta de desenvolvedor". Além disso, inexiste no sistema um mecanismo para que clientes avaliem atendimentos concluídos e para que novos visitantes consultem depoimentos reais, nota média geral e reputação dos serviços prestados. Esta mudança resolve essas dores profissionais através de um redesign simplificado voltado ao usuário e da introdução de um sistema completo de avaliações.

## What Changes

- **Redesign Profissional e Simplificado da Interface**:
  - Remoção de todos os elementos, textos e jargões voltados a desenvolvedores (menções a "Backend Xano", "Camada de Resiliência", "Innovation Lab Impacta", IDs técnicos de sistema expostos ao usuário e mensagens técnicas de depuração).
  - Padronização visual com paleta profissional em tons de azul institucional, cards brancos limpos, tipografia consistente (*Plus Jakarta Sans*), espaçamentos refinados e estados vazios amigáveis em português brasileiro (pt-BR).
  - Garantia de responsividade e legibilidade em dispositivos móveis (smartphones), tablets e computadores de mesa.
  - Mensagens de feedback, validações de formulário e alertas reescritos com linguagem clara, direta e humanizada para o cliente final.

- **Nova Aba Pública de Avaliações**:
  - Exibição aberta de avaliações com nota em estrelas (1 a 5), data de publicação, primeiro nome do cliente (com inicial do sobrenome) e comentário textual.
  - Indicadores destacados de nota média geral e volume total de avaliações computadas.
  - Ordenação por avaliações mais recentes e paginação / controle de carregamento progressivo.
  - Estado vazio informativo e acolhedor quando ainda não houver avaliações registradas.

- **Avaliação Pós-Atendimento pelo Cliente**:
  - Formulário de avaliação disponibilizado exclusivamente para agendamentos com status `concluido`.
  - Acesso direto pelo cliente autenticado em sua aba "Meus Agendamentos".
  - Regra estrita de unicidade: cada atendimento concluído só pode ser avaliado uma única vez e apenas pelo cliente que participou do atendimento.
  - Validações de nota obrigatória (1 a 5 estrelas) e limite de caracteres no comentário, com feedback visual imediato de confirmação.

## Capabilities

### New Capabilities
- `review-system`: Sistema de gestão e exibição pública de avaliações, incluindo agregação de nota média, contagem total de feedbacks e listagem ordenada de avaliações com exibição amigável de clientes.

### Modified Capabilities
- `appointment-engine`: Modificação do ciclo de vida dos agendamentos para incorporar o fluxo de avaliação pós-conclusão pelo cliente e remoção de termos e identificadores técnicos das interfaces de agendamentos.

## Impact

- **Código Afetado**:
  - `app.py`: reformulação visual do cabeçalho, sidebar e abas; inclusão da nova aba de Avaliações; substituição de jargões técnicos por mensagens limpas; inclusão da interface de avaliação nos cards de atendimentos concluídos.
  - `services/appointment_service.py`: inclusão de campos de suporte a status de avaliação em atendimentos e saneamento de mensagens de erro.
  - `services/review_service.py`: novo módulo de serviço para processamento, validação e persistência de avaliações.
  - `services/ui_utils.py`: componentes de renderização de estrelas de avaliação, cards de feedback e remoção de metadados técnicos.
- **APIs e Banco**:
  - Criação/suporte à entidade de `avaliacoes` (vinculada a `agendamento_id`, `cliente_id`, `prestador_id`, `nota`, `comentario`, `criado_em`).
  - Atualização do status ou flag `avaliado: bool` no agendamento para garantia de unicidade.
- **Dependências**: Nenhuma biblioteca externa nova necessária (utiliza Streamlit nativo e componentes existentes).

