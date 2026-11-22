## 1. Módulo de Serviços Financeiros e Motor de Regras

- [ ] 1.1 Criar `services/financial_service.py` com funções para filtragem de atendimentos por período (Hoje, Ontem, 7 dias, 30 dias, Mês Atual e Intervalo Personalizado) considerando estritamente atendimentos com status "concluido" e preservando o `valor_cobrado`, verificando o cálculo correto de faturamento total, quantidade de atendimentos e ticket médio via testes unitários.
- [ ] 1.2 Implementar em `services/financial_service.py` a agregação diária de faturamento e a variação comparativa com o período anterior equivalente, verificando o preenchimento de dias vazios e a prevenção de divisões por zero.
- [ ] 1.3 Implementar em `services/financial_service.py` o motor de sugestões analíticas de portfólio (cálculo de ranking de serviços, ticket médio, participação percentual no faturamento, cruzamento com notas do `review_service`, regras de destaque, combos, horários fracos e trava de segurança para amostragem inferior a 3 atendimentos), verificando as sugestões com cenários controlados.

## 2. Componentes Visuais e Interface no Streamlit

- [ ] 2.1 Adicionar em `services/ui_utils.py` componentes visuais de apoio ao painel financeiro (cards de métricas financeiras com comparativo percentual, formatação monetária e layout dos cards explicativos de sugestões de portfólio), verificando estilo e renderização HTML limpa.
- [ ] 2.2 Integrar a aba "Financeiro" em `app.py` exclusivamente para o perfil de prestador autenticado, contendo o filtro de período, os 4 cartões de métricas, o gráfico diário de faturamento (`st.bar_chart`), a tabela cronológica diária e o detalhamento interativo dos atendimentos concluídos por data selecionada.
- [ ] 2.3 Renderizar na aba "Financeiro" a seção "Sugestões para o Portfólio", exibindo os rankings de faturamento, participação e nota média, juntamente com os cards de recomendações explicáveis ou aviso amigável de dados insuficientes, verificando a atualização em tempo real de acordo com o filtro selecionado.

## 3. Testes Automatizados e Validação

- [ ] 3.1 Criar suíte de testes unitários `test_financial_service.py` validando filtros temporais, isolamento por prestador, cálculo de faturamento sobre status concluído, imutabilidade do valor cobrado e todas as regras determinísticas de sugestão do portfólio, executando com 100% de sucesso.
- [ ] 3.2 Executar a suíte completa de testes de regressão (`test_review_system.py`, `test_appointment_engine.py`, `test_recommendation_engine.py`) e compilação do `app.py`, garantindo integridade e ausência de efeitos colaterais na plataforma.

