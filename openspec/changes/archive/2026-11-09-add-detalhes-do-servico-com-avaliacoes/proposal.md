## Why

Atualmente, o catálogo de serviços do AgendAí apresenta apenas informações básicas em cards resumidos, sem oferecer aos clientes uma visão detalhada sobre o serviço contratado, seu histórico de avaliações e a reputação específica daquele procedimento. Além disso, as avaliações de atendimentos eram tratadas de forma dispersa, sem um vínculo obrigatório e direto com o serviço prestado, e sem uma experiência acolhedora que convide o cliente a avaliar seu atendimento concluído por meio de uma janela modal dedicada no momento apropriado.

Esta proposta introduz a janela modal de detalhes para cada serviço com suas avaliações específicas e estabelece o vínculo mandatório entre cada avaliação e seu respectivo serviço, além de exibir um diálogo de avaliação pós-atendimento quando o serviço for concluído.

## What Changes

- **Botão "Detalhes" e Janela Modal por Serviço**:
  - Inclusão do botão "Detalhes" em cada card de serviço no catálogo.
  - Abertura de janela modal independente (`st.dialog`) contendo: nome, descrição completa, preço formatado em BRL, duração em minutos, resumo com nota média e total de avaliações, listagem cronológica decrescente dos depoimentos daquele serviço específico com paginação ("Carregar Mais"), estado vazio acolhedor e botão direto para agendar o serviço.
- **Vínculo Obrigatório entre Avaliação e Serviço**:
  - Cada avaliação passa a registrar obrigatoriamente o identificador do serviço (`servico_id`), do atendimento (`agendamento_id`) e do cliente.
  - Proibição de avaliações sem serviço associado; toda avaliação passa a pertencer a um serviço específico.
  - Migração resiliente das avaliações pré-existentes no repositório em memória/mock para associá-las ao serviço do agendamento correspondente.
- **Janela Modal de Avaliação Pós-Atendimento**:
  - Quando um agendamento for concluído pelo prestador, o cliente autenticado é recebido com uma janela modal solicitando a avaliação daquele atendimento.
  - O serviço contratado é identificado automaticamente a partir do agendamento concluído (o cliente não escolhe manualmente).
  - Formulário com nota obrigatória (1 a 5 estrelas) e comentário opcional (até 500 caracteres).
  - Opção de fechar o diálogo sem avaliar e ser lembrado posteriormente (através de botão "Avaliar Atendimento" na aba de agendamentos).
  - Bloqueio estrito de reavaliação: cada atendimento concluído só pode ser avaliado uma única vez.
- **Remoção da Aba Geral e Exibição Exclusiva por Serviço**:
  - A aba autônoma "Avaliações" é removida de todas as interfaces (visitante público, cliente e prestador). As notas e depoimentos ficam restritos aos pontos de contato diretos do serviço: na janela modal de "Detalhes" no Catálogo Geral e na seção "Média das avaliações" dos cards de busca do Assistente de Recomendação.

## Capabilities

### New Capabilities
- `review-system`: Gestão e exibição de avaliações vinculadas estritamente a serviços e agendamentos concluídos, agregação de métricas por serviço, validação de unicidade e solicitação modal de feedback pós-atendimento.

### Modified Capabilities
- `service-catalog`: Inclusão da ação "Detalhes" no card de serviço do catálogo, permitindo abrir modal de detalhes com informações completas e listagem contextual de avaliações daquele serviço.

## Impact

- **Código Afetado**:
  - `services/review_service.py`: campos `servico_id` e `servico_titulo`, rotina de migração `migrate_legacy_reviews()`, filtros e cálculos em `get_reviews` e `get_metrics`, e suporte à unicidade por agendamento.
  - `services/ui_utils.py`: componentes visuais de resumo de avaliações por serviço (`service_reviews_summary_html`) e exibição de badge de serviço em `review_card_html`.
  - `app.py`: botão "Detalhes" nos cards de catálogo, modal de detalhes do serviço via `st.dialog`, modal contextual de avaliação pós-atendimento para clientes com atendimentos pendentes de avaliação e filtro por serviço na aba pública.
  - `test_review_system.py`: cobertura de testes para vínculo com serviço, cálculo de médias por serviço, herança automática no agendamento e integridade dos modais.
- **APIs e Banco**:
  - Suporte ao atributo `servico_id` na entidade de avaliações e no endpoint de submissão e consulta.
- **Dependências**: Nenhuma dependência externa adicional; utiliza recursos nativos do Streamlit 1.64 (`st.dialog`).

