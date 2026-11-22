## Context

Atualmente, o AgendAí autentica usuários e mantém a sessão em `st.session_state["user"]` e `st.session_state["auth_token"]`. A barra lateral (`st.sidebar`) exibe o logotipo, o card com iniciais do nome, e-mail e perfil, além do botão de logout. Não existe interface para edição de dados cadastrais, upload de foto, alteração de tema ou troca de senha.

Consulte [proposal.md](proposal.md) para a motivação detalhada e [specs/user-auth/spec.md](specs/user-auth/spec.md) para os critérios normativos de aceitação.

## Goals / Non-Goals

**Goals:**
- Adicionar ícone de engrenagem na barra lateral com acessibilidade, tooltip e navegação fluida para a tela de configurações.
- Implementar tela dedicada de Configurações da Conta com botão "Voltar" que restaura o painel anterior sem perda de contexto.
- Permitir edição de nome e telefone (com validação e máscara brasileira DDD + número).
- Permitir upload de foto de perfil (JPG, PNG, WebP até 2 MB) com recorte circular e prévia, persistência local e opção de remoção voltando às iniciais.
- Fornecer seletor de tema (Claro e Escuro) com persistência no perfil do usuário e injeção dinâmica de CSS com contraste adequado.
- Implementar alteração segura de senha exigindo validação da senha atual e checagem de força da nova senha.
- Ocultar cabeçalhos técnicos do Streamlit (`stHeader`, botões de deploy e menu do desenvolvedor).

**Non-Goals:**
- Alteração de e-mail (permanece estritamente somente leitura por ser a chave de login primária).
- Autenticação de dois fatores (2FA / MFA) ou login social via OAuth (Google, Apple).
- Integração com serviços externos de cloud storage (S3, Cloudinary), utilizando armazenamento local seguro com controle de acesso.

## Decisions

### Decisão 1: Navegação via Estado de Sessão (`st.session_state["view_mode"]`)
- **Escolha**: Controlar a exibição da tela de configurações através de uma variável de estado `st.session_state["view_mode"]` (`"dashboard"` vs `"settings"`).
- **Alternativa considerada**: Uso de múltiplas páginas Streamlit (`pages/configuracoes.py`).
- **Justificativa**: Evita recarga completa do navegador, previne perda de estado da sessão, simplifica o controle de autorização e permite que o botão "Voltar" retorne exatamente à aba e painel onde o usuário estava.

### Decisão 2: Armazenamento Local de Avatares em `uploads/avatars/`
- **Escolha**: Salvar as fotos de perfil em diretório local `uploads/avatars/avatar_user_{id}.png`, gravando o caminho no atributo `photo_url` do usuário. Na exibição, gerar componente HTML seguro com `border-radius: 50%` e `object-fit: cover`.
- **Alternativa considerada**: Armazenamento de grandes strings Base64 diretamente no banco de dados.
- **Justificativa**: Manter os registros de usuários leves, evitar estouro de limites de payload REST e permitir cache eficiente das imagens no navegador.

### Decisão 3: Injeção Dinâmica de CSS para Temas Claro e Escuro
- **Escolha**: Parametrizar a injeção em `ui_utils.py` e eliminar estilos estáticos conflitantes em `app.py` que impunham `#FFFFFF !important` em formulários, inputs e sidebar. No tema escuro:
  - Fundo principal `.stApp`: `#0B0F19`
  - Barra lateral `[data-testid="stSidebar"]` e elementos internos: `#0F172A` / `#1E293B`
  - Formulários `div[data-testid="stForm"]`, cartões e expanders: `#0F172A`
  - Inputs, selects, textareas e botões secundários: `#1E293B` com bordas `#334155`
  - Tipografia integral (h1-h6, saudações "Olá, ...!", labels de formulários e parágrafos): branca `#F8FAFC`
  - Textos secundários/auxiliares: `#94A3B8`
- **Alternativa considerada**: Alteração estática no `.streamlit/config.toml`.
- **Justificativa**: O `config.toml` do Streamlit é global para todo o servidor e requer reinicialização para entrar em vigor. A injeção dinâmica de CSS com controle unificado elimina conflitos de especificidade e permite que cada usuário logado tenha sua preferência individual aplicada imediatamente.

### Decisão 4: Validação Rigorosa de Senha e Segurança
- **Escolha**: Função `change_password(user_id, current_pass, new_pass)` valida a correspondência da senha atual, checa mínimo de 8 caracteres alfanuméricos e atualiza a credencial sem registrar senhas em logs ou terminal.
- **Alternativa considerada**: Permitir redefinição direta sem exigir a senha atual.
- **Justificativa**: Exigir a senha atual é um requisito fundamental de segurança para prevenir alterações indevidas em caso de estações de trabalho compartilhadas.

### Decisão 5: Higienização Visual da Interface
- **Escolha**: Injetar regra CSS ocultando `header[data-testid="stHeader"]`, `#MainMenu` e rodapé padrão do Streamlit.
- **Justificativa**: Elimina distrações técnicas (como botão de "Deploy") e garante aparência limpa e profissional condizente com uma plataforma de produção.

## Risks / Trade-offs

- **[Manipulação de arquivos em sistemas operacionais distintos]**  
  → *Mitigação*: Utilizar `pathlib.Path` ou `os.path.join` para garantir compatibilidade total entre ambientes Windows e Linux.
- **[Conflito de contraste em elementos específicos no tema escuro]**  
  → *Mitigação*: Definir variáveis CSS globais de alta especificidade para inputs (`.stTextInput input`, `.stSelectbox`), tabelas e cards.

