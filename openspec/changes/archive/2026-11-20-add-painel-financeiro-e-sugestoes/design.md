## Context

Atualmente, o sistema AgendAí registra agendamentos contendo `cliente_id`, `prestador_id`, `servico_id`, `servico_titulo`, `data`, `hora_inicio`, `duracao_minutos`, `valor_cobrado` e `status` (`pendente`, `confirmado`, `concluido`, `cancelado`). O módulo `review_service.py` armazena avaliações com notas de 1 a 5 vinculadas ao `servico_id`.

No entanto, inexiste um módulo de agregação financeira e inteligência de portfólio. As interfaces do prestador em `app.py` disponibilizavam apenas métricas simplificadas na aba "Resumo" (agendamentos de hoje e preço médio simples do catálogo). Este design estabelece a arquitetura para o novo módulo financeiro e motor de sugestões de portfólio.

## Goals / Non-Goals

**Goals:**
- Criar a camada `services/financial_service.py` com funções puras e determinísticas para agregação de faturamento diário, ticket médio e cruzamento com avaliações.
- Suportar filtros temporais flexíveis (Hoje, Ontem, Últimos 7 dias, Últimos 30 dias, Mês Atual e Intervalo Personalizado) respeitando o fuso horário de Brasília (`America/Sao_Paulo`).
- Apresentar gráfico temporal de barras/linhas do faturamento diário e detalhamento granular por dia via interface Streamlit.
- Construir motor de sugestões de portfólio fundamentado em dados comprovados e regras transparentes (sem suposições ou alucinações).
- Proteger 100% o acesso à camada financeira, restringindo-a exclusivamente ao prestador autenticado e isolando seus dados.

**Non-Goals:**
- Integração com gateways de pagamento bancário (Stripe, Pagar.me, Mercado Pago, etc.).
- Emissão de notas fiscais eletrônicas (NF-e).
- Gestão de custos fixos, estoque ou folha de pagamento de funcionários.
- Alteração automática de preços ou exclusão automática de serviços no catálogo (as sugestões são 100% consultivas).
- Galeria multimídia de fotos de cortes ou trabalhos.

## Decisions

### Decisão 1: Módulo Dedicado `services/financial_service.py`
- **Escolha**: Isolar toda a lógica de agregação financeira, cálculo de ticket médio, agrupamento cronológico e motor de regras de sugestão em um módulo separado (`services/financial_service.py`).
- **Alternativa considerada**: Adicionar as funções dentro de `appointment_service.py` ou diretamente no script `app.py`.
- **Justificativa**: Manter o princípio de responsabilidade única (SRP), permitir testes unitários isolados com 100% de cobertura e evitar sobrecarregar o script de interface `app.py`.

### Decisão 2: Motor Determinístico e Transparente de Sugestões de Portfólio
- **Escolha**: Implementar regras explicáveis baseadas em limites quantitativos:
  1. *Destaque / Preço*: Atendimentos do serviço > média geral E nota média ≥ 4.5.
  2. *Promoção / Combo / Revisão*: Atendimentos < 10% da média do catálogo no período.
  3. *Atenção à Qualidade*: Nota média < 4.0 (com pelo menos 1 avaliação).
  4. *Ociosidade*: Dia da semana ou turno com menor número relativo de agendamentos.
  5. *Trava de Confiabilidade*: Mínimo de 3 atendimentos concluídos no período analisado para gerar sugestões; abaixo disso, exibe estado acolhedor de "Amostra insuficiente".
- **Alternativa considerada**: Usar chamadas a LLMs externos para inventar textos de recomendação.
- **Justificativa**: Evita alucinações, garante repetibilidade, transparência e velocidade instantânea de renderização sem custos de API ou latência de rede.

### Decisão 3: Gráficos Nativos e Responsivos com Streamlit
- **Escolha**: Utilizar `st.bar_chart` ou visualizações nativas do Streamlit alimentadas por estruturas de dados limpas (`pandas.DataFrame` ou dicionários formatados).
- **Alternativa considerada**: Bibliotecas externas pesadas ou renderização de imagens estáticas matplotlib.
- **Justificativa**: Fluidez de renderização, visual profissional moderno alinhado ao design system e total compatibilidade com a stack Streamlit obrigatória do projeto.

### Decisão 4: Controle Estrito de Autorização por Perfil e Sessão
- **Escolha**: Renderizar a aba "Financeiro" unicamente quando `st.session_state["user"]["role"] == "prestador"`. Todas as consultas de dados filtram obrigatoriamente pelo `user["id"]` do prestador da sessão ativa.
- **Alternativa considerada**: Exibir a aba com aviso de bloqueio para clientes.
- **Justificativa**: A privacidade financeira é crítica; clientes não devem sequer tomar ciência da existência ou estrutura de relatórios de faturamento.

## Risks / Trade-offs

- **[Risco] Agendamentos legados sem `valor_cobrado` explícito**  
  → *Mitigação*: A função de recuperação aplicará fallback automático: se `valor_cobrado` for nulo, busca o preço atual do serviço associado em `servicos_cache` ou adota `0.0`, prevenindo erros de cálculo.
- **[Risco] Divisão por zero em períodos com zero atendimentos**  
  → *Mitigação*: Funções de cálculo de ticket médio e participação percentual verificam explicitamente se o divisor é zero, retornando `0.0` com segurança.
- **[Risco] Inconsistências de data decorrentes de fuso horário**  
  → *Mitigação*: Todas as operações de datas utilizam o fuso padrão de Brasília (`America/Sao_Paulo` ou `timezone(timedelta(hours=-3))`) para determinar o que é "Hoje", "Ontem" e os limites de períodos.

