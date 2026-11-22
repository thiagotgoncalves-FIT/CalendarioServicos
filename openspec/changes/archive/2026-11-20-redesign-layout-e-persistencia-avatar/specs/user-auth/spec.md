## MODIFIED Requirements

### Requirement: Gerenciamento e Persistência da Sessão
O sistema MUST reter o estado de autenticação do usuário durante a navegação entre as páginas do frontend Streamlit, garantindo a reconciliação e persistência de dados cadastrais essenciais, incluindo a foto de perfil (avatar) salva no disco (`uploads/avatars/avatar_user_{id}.*`).

#### Scenario: Manutenção da Sessão Ativa
- **WHEN** o usuário autenticado navega por diferentes seções ou interage com elementos da interface
- **THEN** o sistema preserva o token JWT e as informações do usuário em `st.session_state` sem solicitar novo login

#### Scenario: Encerramento de Sessão (Logout)
- **WHEN** o usuário clica na opção "Sair" ou "Logout"
- **THEN** o sistema remove o token JWT e os dados da sessão e retorna o usuário à tela pública inicial

#### Scenario: Persistência e Reconciliação do Avatar no Re-login
- **WHEN** um usuário que possui avatar salvo em disco efetua login novamente após logout ou reinicialização
- **THEN** o sistema detecta o arquivo de avatar correspondente ao `user_id` em `uploads/avatars/`, vincula o caminho a `photo_url` no objeto de usuário e exibe a imagem no perfil sem reverter para iniciais
