## Context

O sistema AgendAí utiliza Streamlit (v1.64.0) no frontend e uma camada de serviços em Python (`services/`) conectada à API REST / Xano com camada de resiliência em memória. A versão atual do catálogo de serviços exibe apenas cards simplificados com agendamento direto via popover. Para detalhes adicionais, ver `proposal.md`.

## Goals / Non-Goals

**Goals:**
- Prover modal dedicado (`@st.dialog`) para visualização de detalhes de cada serviço individualmente com avaliações contextuais e botão direto de agendamento.
- Prover modal dedicado (`@st.dialog`) para convidar o cliente a avaliar seu atendimento concluído de forma automática e acolhedora, com opção de adiar.
- Estabelecer a obrigatoriedade do vínculo `servico_id` em toda avaliação cadastrada ou consultada na plataforma.
- Migrar retroativamente avaliações pré-existentes sem perda de integridade.

**Non-Goals:**
- Criação de fluxo de moderação manual prévia (avaliações continuam sendo publicadas diretamente após validação de formato e unicidade).
- Permitir submissão de avaliações avulsas por usuários que não contrataram e concluíram o serviço.

## Decisions

### Decisão 1: Modais Nativos via `@st.dialog` em vez de Popovers Aninhados
- **Escolha**: Utilizar a API nativa `@st.dialog` do Streamlit 1.64 tanto para a janela "Detalhes do Serviço" quanto para a janela "Avaliar Atendimento".
- **Alternativas Consideradas**: `st.popover` aninhado dentro do card de serviço ou expansão de acordeão (`st.expander`).
- **Motivação**: O `@st.dialog` renderiza um modal centralizado com fundo escurecido (backdrop), isolamento de escopo visual, botão de fechar nativo e excelente experiência em dispositivos móveis e desktop, sem poluir a grade do catálogo.

### Decisão 2: Identificação Automática do Serviço pelo Agendamento
- **Escolha**: O endpoint/função `submit_review` extrai e herda o `servico_id` e `servico_titulo` diretamente a partir do objeto do `agendamento_id` concluído.
- **Alternativas Consideradas**: Apresentar um campo `st.selectbox` para o cliente selecionar o serviço no momento da avaliação.
- **Motivação**: Evita fraudes, inconsistências e esforço desnecessário do usuário; o sistema já tem o registro exato do serviço que foi contratado e executado naquele atendimento.

### Decisão 3: Migração em Memória Transparente (`migrate_legacy_reviews`)
- **Escolha**: Executar a rotina `migrate_legacy_reviews()` na inicialização do módulo `review_service.py` para enriquecer avaliações legadas com `servico_id` e `servico_titulo`.
- **Alternativas Consideradas**: Excluir avaliações anteriores sem serviço.
- **Motivação**: Preserva o histórico de dados dos clientes e evita valores nulos ou erros de chave ao calcular médias por serviço.

### Decisão 4: Persistência do Fechamento do Modal de Avaliação na Sessão
- **Escolha**: Ao fechar o modal de avaliação sem submeter, armazenar uma chave em `st.session_state` para não incomodar o cliente a cada clique na mesma sessão, mantendo o botão "Avaliar Atendimento" visível na aba "Meus Agendamentos".
- **Alternativas Consideradas**: Reabrir o modal a cada navegação de página.
- **Motivação**: Garante uma experiência de usuário agradável e respeitosa, sem forçar interrupções indesejadas.

### Decisão 5: Remoção da Aba Geral em favor de Visualização 100% Contextual
- **Escolha**: Eliminar a aba geral autônoma de avaliações, concentrando os depoimentos e notas médias exclusivamente no modal de "Detalhes" do Catálogo Geral e na seção "Média das avaliações" dos cards de recomendação.
- **Motivação**: Reduz a sobrecarga de abas na barra de navegação e evita dispersão, apresentando o feedback social no momento exato em que o cliente está decidindo contratar aquele serviço específico.

## Risks / Trade-offs

- **[Risco] Reimportação / cache de módulos em execução Streamlit** → **Mitigação**: Desenhar `get_metrics` e `get_reviews` com parâmetros opcionais (`servico_id: Optional[int] = None`) com valores padrão seguros, garantindo que qualquer chamada sem parâmetros continue operando normalmente sem `TypeError`.
- **[Risco] Concorrência ou duplo clique no modal de avaliação** → **Mitigação**: Validação de unicidade estrita em `services/review_service.py` via `is_appointment_reviewed` antes de persistir, rejeitando tentativas duplicadas.

## Migration Plan

1. Executar `migrate_legacy_reviews()` no `services/review_service.py`.
2. Assegurar que consultas públicas sem `servico_id` continuem calculando a nota consolidada geral.
3. Testar a regressão com a suíte existente de testes unitários.

