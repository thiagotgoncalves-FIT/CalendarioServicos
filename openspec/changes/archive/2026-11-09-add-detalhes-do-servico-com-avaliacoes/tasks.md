## 1. Camada de Serviço e Modelagem de Dados

- [x] 1.1 Atualizar `services/review_service.py` adicionando suporte aos campos `servico_id` e `servico_titulo`, implementando a rotina `migrate_legacy_reviews()` para enriquecimento automático de avaliações em memória, verificando a preservação dos dados pré-existentes via testes unitários.
- [x] 1.2 Atualizar as funções `get_reviews` e `get_metrics` com parâmetros opcionais seguros (`servico_id: Optional[int] = None`) e herança automática de `servico_id` em `submit_review` a partir do agendamento, verificando que chamadas legadas continuam funcionando sem `TypeError`.

## 2. Componentes Visuais e Modal de Detalhes do Serviço

- [x] 2.1 Adicionar em `services/ui_utils.py` componentes para resumo de notas e avaliações do serviço (`service_reviews_summary_html`) e exibição contextual de badge do serviço em `review_card_html`, verificando layout limpo e responsivo.
- [x] 2.2 Implementar a janela modal `@st.dialog("Detalhes do Serviço")` em `app.py` exibindo nome, descrição, valor formatado em BRL, duração em minutos, resumo com nota média e total de avaliações, listagem cronológica decrescente com paginação e botão de agendamento.
- [x] 2.3 Atualizar os cards de serviços do catálogo em `app.py` para incluir o botão "Detalhes" alinhado lado a lado ao botão de agendar, verificando a abertura independente para cada serviço.

## 3. Fluxo de Avaliação Pós-Atendimento e Aba Geral

- [x] 3.1 Implementar a janela modal `@st.dialog("Avalie seu Atendimento")` em `app.py` acionada de forma contextual para o cliente autenticado que possui atendimento concluído pendente de avaliação, com nota obrigatória de 1 a 5 estrelas, comentário opcional de até 500 caracteres, bloqueio de reavaliação e opção de avaliar mais tarde.
- [x] 3.2 Disponibilizar o botão "Avaliar Atendimento" no card do agendamento concluído na aba "Meus Agendamentos", permitindo que o cliente abra o modal caso tenha fechado a janela anteriormente.
- [x] 3.3 Remover a aba geral de avaliações em `app.py` (nas interfaces do cliente, prestador e visitante público), mantendo a exibição de notas e depoimentos exclusivamente no modal de Detalhes do Catálogo e nos cards da Pesquisa de Serviços.

## 4. Testes Automatizados e Validação

- [x] 4.1 Atualizar a suíte de testes `test_review_system.py` cobrindo submissão com herança automática de serviço, cálculo de métricas isoladas por serviço, unicidade de avaliação e prevenção de reavaliação, executando com 100% de sucesso.
- [x] 4.2 Executar testes de regressão existentes (`test_appointment_engine.py`, `test_recommendation_engine.py`) garantindo estabilidade, integridade e ausência de regressões na plataforma.

