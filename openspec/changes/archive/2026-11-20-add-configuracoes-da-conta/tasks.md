## 1. Camada de Serviço e Gestão de Usuário

- [x] 1.1 Implementar em `services/auth_service.py` as funções `update_user_profile(user_id, name, phone)` e `change_password(user_id, current_password, new_password)` com validação rigorosa de nome, telefone com máscara brasileira e força de senha (mínimo 8 caracteres alfanuméricos), verificando a atualização correta via testes unitários.
- [x] 1.2 Implementar em `services/auth_service.py` as rotinas `save_user_avatar(user_id, image_bytes, filename)` (com validação de formato JPG/PNG/WebP, limite de até 2 MB e persistência em `uploads/avatars/`) e `remove_user_avatar(user_id)`, verificando a criação, gravação e remoção segura de arquivos em disco.
- [x] 1.3 Implementar em `services/auth_service.py` a função `update_user_theme(user_id, theme)` para persistência da preferência de aparência (Claro / Escuro) no cadastro do usuário e no estado de sessão, verificando a preservação da escolha.

## 2. Componentes Visuais e Injeção de Temas

- [x] 2.1 Adicionar em `services/ui_utils.py` suporte a avatar circular customizado em `user_avatar_html(user, size)` (renderizando a imagem com recorte centralizado quando existir ou as iniciais nominais como fallback), verificando a renderização visual em diferentes tamanhos.
- [x] 2.2 Implementar em `services/ui_utils.py` o injetor de estilos dinâmicos `apply_theme_and_clean_ui(theme_name)` com tokens de alto contraste para os temas Claro e Escuro e ocultação de elementos técnicos nativos do Streamlit (`header[data-testid="stHeader"]`, botões de deploy e menu técnico).
- [x] 2.3 Refinar as regras de CSS em `services/ui_utils.py` e `app.py` eliminando blocos de estilo estáticos conflitantes (#FFFFFF !important), assegurando que o Tema Escuro cubra 100% da barra lateral, formulários e inputs com fundos escuros e tipografia branca (#F8FAFC).

## 3. Interface da Barra Lateral e Tela de Configurações

- [x] 3.1 Atualizar a barra lateral em `app.py` adicionando o botão de engrenagem clicável no card de perfil ativo com acessibilidade e tooltip, integrando a alternância do estado `st.session_state["view_mode"]` para todos os perfis autenticados.
- [x] 3.2 Implementar em `app.py` a tela de Configurações da Conta com botão "Voltar", seção de foto de perfil (com prévia circular imediata e botão de remoção), seção de dados pessoais (edição de nome, telefone com máscara e e-mail somente leitura) e atualização imediata do cabeçalho e saudação.
- [x] 3.3 Implementar na tela de Configurações em `app.py` o seletor de tema (Claro / Escuro) com alternância dinâmica de estilos e a seção de Segurança para alteração de senha (exigindo senha atual e checagem de força), verificando proteção contra vazamento de credenciais em logs.

## 4. Testes Automatizados e Validação

- [x] 4.1 Criar a suíte de testes unitários `test_user_settings.py` cobrindo atualização de dados de perfil, validação de telefone, upload e exclusão de avatar, persistência de tema e fluxo de alteração de senha, executando com 100% de sucesso.
- [x] 4.2 Executar a suíte completa de testes de regressão (`test_review_system.py`, `test_appointment_engine.py`, `test_recommendation_engine.py`) e compilação do `app.py`, garantindo estabilidade geral e ausência de regressões na plataforma.

