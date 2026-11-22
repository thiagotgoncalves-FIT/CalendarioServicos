## 1. Frente C — Desacoplamento da Autenticação e Página Exclusiva de Cadastro

- [x] 1.1 Refatorar a renderização da área pública em `app.py`, eliminando abas e implementando navegação exclusiva via estado `st.session_state["auth_page"]` ("login" ou "signup")
- [x] 1.2 Implementar página de Login com link em destaque *"Não tem uma conta? Criar conta"*, direcionando para o cadastro com transição limpa
- [x] 1.3 Implementar página exclusiva de Cadastro com campos de Nome, E-mail, Senha, Confirmação de Senha, Telefone e Perfil (`cliente` ou `prestador`), incluindo link *"Já tem uma conta? Entrar"*
- [x] 1.4 Adicionar validação estrita de confirmação de senha no frontend e manter integração segura com hash de senhas no Xano via `auth_service.py`

## 2. Frente A — Assistente Inteligente de Recomendação

- [x] 2.1 Criar o módulo `services/recommendation_service.py` implementando o algoritmo de pontuação multicritério normalizado (0 a 100) com pesos configuráveis (serviço 35%, orçamento 25%, disponibilidade 25%, avaliação 15%)
- [x] 2.2 Implementar no serviço de recomendação os filtros excludentes obrigatórios: desclassificação sumária de prestadores acima do orçamento máximo ou sem horários livres na data desejada
- [x] 2.3 Adicionar a aba/seção do Assistente Inteligente no painel do cliente em `app.py`, com formulário de busca, listagem ordenada dos prestadores recomendados e justificativa explicativa dos fatores de pontuação
- [x] 2.4 Integrar atalho direto nos cards de recomendação para seleção de horário livre e confirmação imediata da reserva através do motor de agendamentos

## 3. Frente B — Redesign Visual Completo da Aplicação

- [x] 3.1 Atualizar o CSS customizado e utilitários visuais em `services/ui_utils.py` e `.streamlit/config.toml` com tipografia consistente, paleta refinada e espaçamentos uniformes
- [x] 3.2 Refatorar visualmente os cards de serviços, cards de prestadores recomendados e formulários em todas as páginas, eliminando excessos decorativos
- [x] 3.3 Padronizar mensagens de feedback, estados vazios acolhedores, spinners de carregamento e toasts de sucesso/alerta em todas as telas

## 4. Testes e Validação Integrada

- [x] 4.1 Criar testes automatizados em `test_recommendation_engine.py` cobrindo cálculo de score, exclusão por orçamento, exclusão por data ocupada e justificativas
- [x] 4.2 Executar testes de integração e validar o funcionamento das telas de login/cadastro, portal do cliente e portal do prestador
- [x] 4.3 Executar validação estrita do OpenSpec com `openspec validate --specs` garantindo conformidade arquitetural
