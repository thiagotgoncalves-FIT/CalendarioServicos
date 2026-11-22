## Why

Atualmente, os usuários autenticados da plataforma AgendAí (tanto Prestadores quanto Clientes) não possuem uma tela para gerenciar as configurações de sua própria conta. Não é possível atualizar nome, telefone, alterar a foto de perfil, escolher entre tema claro ou escuro com persistência, nem redefinir sua senha de acesso. A barra lateral exibe apenas informações estáticas do perfil ativo e o botão de sair. Esta proposta introduz a tela de Configurações da Conta acessível via ícone de engrenagem na barra lateral, oferecendo autonomia e personalização com segurança.

## What Changes

- **Engrenagem de Configurações na Barra Lateral**:
  - Inclusão de botão/ícone de engrenagem clicável no card "Perfil Ativo" da barra lateral, com acessibilidade (`Configurações`), tooltip e foco visual.
  - Acesso universal para todos os perfis autenticados (`prestador` e `cliente`).
  - Navegação fluida para a tela independente de Configurações, contendo botão "Voltar" que retorna à visualização anterior.
- **Gestão de Foto de Perfil**:
  - Exibição de avatar circular com recorte centralizado.
  - Upload de imagens nos formatos JPG, PNG e WebP com validação de limite de tamanho de até 2 MB.
  - Pré-visualização imediata antes de salvar e persistência segura em pasta local (`uploads/avatars/`) com referência no cadastro do usuário.
  - Opção para remover a foto e restaurar as iniciais nominais.
  - Atualização instantânea do avatar na barra lateral e em todas as referências do sistema.
- **Edição de Dados Pessoais**:
  - Campo editável para nome completo (obrigatório, com validação de tamanho).
  - Campo editável para telefone com máscara brasileira (DDD + número), normalização e validação.
  - Campo de e-mail exibido como somente leitura (preservando a integridade da credencial primária de acesso).
  - Botão "Salvar alterações" com mensagens de feedback amigáveis em pt-BR e atualização imediata do nome na saudação ("Olá, ...!") e no card da barra lateral.
- **Personalização de Aparência (Tema)**:
  - Seletor de tema com opções **Claro** e **Escuro**.
  - Aplicação imediata de estilos CSS dinâmicos com contraste e legibilidade em todas as telas, cards, abas, janelas modais e formulários.
  - Persistência da preferência na conta do usuário (`user["theme"]`), mantendo a escolha em novos logins e sessões.
- **Segurança da Conta (Alteração de Senha)**:
  - Seção para troca de senha exigindo a confirmação da senha atual.
  - Validação de nova senha com critérios mínimos de segurança (mínimo de 8 caracteres contendo letras e números).
  - Armazenamento seguro de hash e proteção absoluta contra vazamento ou log de credenciais sensíveis.
- **Higiene Visual e Responsividade**:
  - Ocultação de elementos técnicos nativos do Streamlit (como botões de deploy e barra superior técnica) para o usuário final.
  - Layout totalmente responsivo para dispositivos móveis, tablets e desktops.

## Capabilities

### New Capabilities
*(Nenhuma nova capability isolada criada; a funcionalidade expande naturalmente o ciclo de identidade, perfil e tema já existente em `user-auth`)*

### Modified Capabilities
- `user-auth`: Adiciona requisitos normativos para navegação via engrenagem da barra lateral, edição de dados pessoais e foto de perfil, persistência de tema (Claro/Escuro) e alteração segura de senha.

## Impact

- **Frontend (`app.py`)**:
  - Inclusão do botão de engrenagem no card de perfil da barra lateral (`st.sidebar`).
  - Implementação da tela/estado independente de Configurações da Conta com navegação reversa ("Voltar").
  - Injeção de CSS para suporte refinado aos temas Claro e Escuro e ocultação de elementos técnicos do Streamlit.
- **Serviços (`services/auth_service.py` e `services/ui_utils.py`)**:
  - Funções para atualização de perfil do usuário (`update_user_profile`), upload e remoção de avatar (`save_user_avatar`, `remove_user_avatar`), alteração de senha (`change_password`) e persistência do tema.
  - Adaptação dos helpers de avatar e estilos em `ui_utils.py` para suportar imagem customizada ou iniciais nominais.
- **Persistência e Arquivos**:
  - Criação da pasta de armazenamento de avatares `uploads/avatars/`.
  - Armazenamento seguro dos novos campos (`photo_url`, `theme`) preservando retrocompatibilidade total com contas já cadastradas.

