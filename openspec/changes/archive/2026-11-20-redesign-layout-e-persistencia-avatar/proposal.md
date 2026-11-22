## Why

O layout da barra lateral atualmente posiciona o bloco de perfil e as opções em seções separadas abaixo da marca, gerando espaçamento vertical desnecessário. Além disso, as fotos de perfil (avatares) salvas pelos usuários não estão persistindo após o logout ou ao logar novamente: como o login subsequente consulta a base sem reconciliar o arquivo de imagem salvo em disco (`uploads/avatars/avatar_user_{id}.*`), o caminho da foto é perdido na sessão, revertendo indevidamente para as iniciais.

## What Changes

- **Reposicionamento do Usuário Logado na Barra Lateral**:
  - Reorganizar a parte superior da barra lateral esquerda, posicionando as informações do usuário autenticado (avatar compacto, nome, e-mail e badge de papel) de forma harmoniosa logo abaixo ou em integração direta com a marca e nome do projeto "AgendAí", eliminando rolagem desnecessária.
- **Botão de Recolher/Expandir e Modo Mini Barra Lateral**:
  - Preservar a visibilidade do botão de alternância (collapse/expand button do Streamlit) mesmo quando a barra estiver recolhida, sem ser ocultado pela higienização do header.
  - Configurar visualização retrátil em modo "mini barra lateral" (largura compacta com ícones destacados), evitando que a lateral seja completamente ocultada sem controle de reabertura.
- **Persistência Confiável do Avatar de Usuário**:
  - Garantir que a imagem salva localmente em `uploads/avatars/avatar_user_{id}.*` seja automaticamente recuperada e vinculada ao objeto de usuário durante a autenticação (`login` e `get_current_user`), preservando a foto ativa mesmo após logout, reinicialização ou login em sessão limpa.
  - Sincronização do caminho relativo e absoluto da foto no dicionário do usuário retornado na autenticação.

## Capabilities

### Modified Capabilities
- `user-auth`: Garantir persistência e reconciliação da foto de perfil ativa (`photo_url`) no login e sessão do usuário.
- `prestador-dashboard`: Reorganizar o cabeçalho superior da barra lateral unificando a marca "AgendAí" com a identificação do usuário autenticado.

## Impact

- **Código Afetado**: `app.py` (layout e hierarquia da barra lateral), `services/auth_service.py` (reconciliação de avatar ao logar e obter usuário atual), `services/ui_utils.py` (renderização e dimensões do avatar na barra lateral).
- **APIs / Dados**: Compatibilidade preservada com Xano e modo resiliente local. Nenhuma quebra de contrato na API.
