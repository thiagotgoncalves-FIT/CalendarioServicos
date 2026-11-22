## Why

Para transformar o AgendAí em um marketplace moderno e competitivo de serviços freelancers, é fundamental elevar a experiência de descoberta e contratação de profissionais. Clientes atualmente precisam buscar manualmente em um catálogo estático, a interface carece de padronização visual contemporânea e o fluxo de autenticação utiliza abas na mesma tela, gerando fricção. Esta mudança introduz um assistente inteligente de recomendação baseado em pontuação multicritério (0 a 100), reformula integralmente o design visual de todas as telas em Streamlit e desacopla a autenticação em páginas exclusivas de Login e Cadastro conectadas por links diretos.

## What Changes

- **Frente A — Assistente Inteligente de Recomendação**:
  - Nova interface de recomendação no fluxo do cliente onde é possível especificar serviço, descrição da necessidade, orçamento máximo e data/período desejado.
  - Algoritmo de scoring normalizado (0 a 100) ponderando compatibilidade textual/serviço, teto orçamentário, disponibilidade real de agenda e avaliação média do prestador.
  - Filtros excludentes obrigatórios: prestadores sem agenda livre na data ou com preço acima do orçamento são desclassificados (sem dados fictícios).
  - Justificativas explicativas transparentes exibidas em cada card de profissional recomendado.
  - Acesso direto ao perfil do profissional e início imediato do fluxo de agendamento validado.
- **Frente B — Redesign Visual Completo da Aplicação**:
  - Padronização estética profissional em todas as telas (login, cadastro, painel do cliente, catálogo, assistente, painel do prestador, agenda e resumo).
  - Design system unificado com tipografia moderna, hierarquia clara, paleta escura refinada, componentes consistentes de cards, formulários e métricas.
  - Feedback visual aprimorado: estados vazios encorajadores, loaders e toasts de notificação, eliminando excesso de emojis e bordas pesadas.
  - Criação de componentes visuais reutilizáveis em `services/ui_utils.py` ou módulo de componentes.
- **Frente C — Novo Fluxo de Autenticação e Página Exclusiva de Cadastro**:
  - Eliminação total de abas para alternar entre Login e Cadastro na mesma tela.
  - Página de Login dedicada com botão de entrada e link destacado *"Não tem uma conta? Criar conta"*.
  - Página exclusiva de Cadastro independente com campos de Nome, E-mail, Senha, Confirmação de Senha, Telefone e Seleção de Papel (`cliente` / `prestador`), com link de retorno *"Já tem uma conta? Entrar"*.
  - Navegação nativa e fluida baseada no estado da aplicação Streamlit (`st.session_state["auth_page"]` ou roteamento equivalente), mantendo validação segura de senhas (mínimo 8 caracteres com letras e números) e hash criptográfico no backend Xano.

## Capabilities

### New Capabilities
- `smart-recommendation`: Assistente inteligente de recomendação de prestadores com algoritmo de pontuação multicritério (0-100), filtros estritos de orçamento/disponibilidade e justificativas transparentes.
- `marketplace-ui`: Design system e componentes visuais padronizados para todas as páginas da aplicação (cards modernos, formulários, estados vazios e layout responsivo).

### Modified Capabilities
- `user-auth`: Desacopla autenticação em telas exclusivas e independentes de Login e Cadastro sem uso de abas, com navegação por links e validação completa integrada ao Xano.

## Impact

- **Frontend (`app.py`, `services/ui_utils.py`)**:
  - Roteamento visual para alternar de forma limpa entre Login e Cadastro sem abas.
  - Nova aba ou seção do Assistente Inteligente de Recomendação no portal do cliente.
  - Reestilização de todos os containers, cards de serviços e formulários existentes.
- **Serviços (`services/recommendation_service.py`, `services/auth_service.py`)**:
  - Novo serviço de recomendação encapsulando o algoritmo determinístico de pontuação e filtragem.
  - Ajustes nas chamadas de autenticação e validação de senhas com confirmação.
- **Backend (Xano)**:
  - Reutilização dos endpoints existentes de `auth`, `service_catalog`, `prestador_availability` e `appointments`. Nenhuma quebra de retrocompatibilidade.
