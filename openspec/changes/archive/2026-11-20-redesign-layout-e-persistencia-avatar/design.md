## Context

Ver `proposal.md` para a motivação. Atualmente:
1. No arquivo `services/auth_service.py`, a função `save_user_avatar` grava os bytes da imagem na pasta `uploads/avatars/avatar_user_{user_id}{ext}` e salva o caminho no registro em memória `_MOCK_USERS_DB`. No entanto, quando o usuário faz login novamente através de `login(email, password)` ou quando `get_current_user(token)` é chamado, os dados vêm do Xano (ou de registros não reconciliados), onde o campo `photo_url` ou não existe no retorno ou vem nulo. Como o sistema não verifica se o arquivo correspondente já existe no disco para aquele `user_id`, a sessão perde a foto salva.
2. Na barra lateral de `app.py`, o bloco de identificação do usuário logado é renderizado com espaçamentos largos após a marca da plataforma, ocupando espaço vertical precioso e afastando o perfil do topo visual da aplicação.

## Goals / Non-Goals

**Goals:**
- Implementar uma função auxiliar de reconciliação em `services/auth_service.py` (ex.: `_enrich_user_avatar(user_dict)`) que checa no diretório `uploads/avatars/` se existe um arquivo de avatar para o `id` do usuário. Se existir, preenche automaticamente `photo_url` e `photo_rel_url`.
- Chamar a reconciliação em todos os pontos de retorno de usuário: `login`, `signup`, `get_current_user` e `update_user_profile`.
- Reestruturar o cabeçalho da barra lateral em `app.py` integrando o nome/marca do projeto e o perfil do usuário logado em uma área superior coesa e limpa, mais alta na tela.

**Non-Goals:**
- Não alterar provedores externos de armazenamento de mídia ou bancos de dados cloud (continua usando persistência local em `uploads/avatars/`).
- Não alterar as permissões de upload nem os limites existentes (2 MB, extensões JPG/PNG/WebP).

## Decisions

1. **Reconciliação Local Determinística por ID de Usuário**:
   - *Decisão*: Ao processar qualquer dicionário de usuário na camada de autenticação, verificar se existe `avatar_user_{user_id}.*` em `uploads/avatars/`.
   - *Alternativas consideradas*: Salvar o caminho no `localStorage` do navegador ou depender exclusivamente do retorno do Xano. A verificação direta no disco é imediata, segura e funciona perfeitamente mesmo quando o Xano não possui o campo avatar configurado.

2. **Reorganização Visual da Barra Lateral Superior**:
   - *Decisão*: Unificar o logotipo/nome do AgendAí e o cartão do usuário ativo no topo da sidebar em um contêiner limpo com hierarquia visual clara e espaçamento reduzido.
   - *Alternativas consideradas*: Mover o perfil para o rodapé da sidebar. O usuário solicitou explicitamente manter o usuário logado à esquerda e mais para cima, junto ao nome do projeto.

3. **Preservação do Botão de Toggle e Modo Mini Sidebar**:
   - *Decisão*: Ajustar o CSS de higienização em `services/ui_utils.py` para não ocultar o botão de controle da sidebar (`div[data-testid="stSidebarCollapsedControl"]`). Adicionar estilização que mantém a barra recolhida exibindo uma mini coluna de ícones.
   - *Alternativas consideradas*: Travar a barra lateral como sempre expandida (`initial_sidebar_state="expanded"` sem recolhimento). Manter o recolhimento com botão visível e ícones é a melhor experiência de usuário.

## Risks / Trade-offs

- **[Risco] Múltiplos formatos de imagem salvos para o mesmo ID** → **Mitigação**: Na remoção e na resolução do avatar, fazer busca ordenada pelas extensões suportadas (`.png`, `.jpg`, `.jpeg`, `.webp`) e na gravação de nova imagem remover previamente quaisquer arquivos antigos daquele ID.
- **[Risco] Renderização no Streamlit após logout/login** → **Mitigação**: Assegurar que `do_logout` e a tela de login reinicializem adequadamente o estado sem cache residual indesejado.
