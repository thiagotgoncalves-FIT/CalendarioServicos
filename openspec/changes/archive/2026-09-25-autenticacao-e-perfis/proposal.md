## Why

Para que o **AgendAí** funcione com segurança e personalização, é necessário identificar e autenticar os dois públicos da plataforma: o **Prestador de Serviços** (que gerencia seus serviços e agenda) e o **Cliente** (que visualiza catálogos e realiza reservas). Sem autenticação e segregação de perfis (`role`), não é possível proteger os dados dos prestadores, restringir ações administrativas ou associar agendamentos aos seus respectivos solicitantes.

Esta fatia inicial estabelece a fundação de segurança no Xano (tabela `user`, criptografia de senha e emissão de tokens JWT) e a interface de acesso no Streamlit (login, cadastro e controle de sessão), viabilizando as próximas fatias de catálogo e agendamento.

## What Changes

- Criação e configuração da tabela `user` no banco de dados do Xano com campos para identificação, contato e perfil de acesso (`role`).
- Implementação de endpoints REST no Xano para registro de novos usuários (`POST /auth/signup`), login (`POST /auth/login`) e consulta do perfil autenticado (`GET /auth/me`).
- Criação de interface de autenticação no frontend Streamlit com abas de **Login** e **Cadastro**, incluindo seleção clara de perfil ("Prestador" ou "Cliente").
- Implementação de gerenciamento de sessão via `st.session_state` para reter o token JWT e dados do usuário logado durante a navegação.
- Tratamento de mensagens amigáveis de erro para falhas de validação (ex.: e-mail já cadastrado, senha incorreta, campos obrigatórios não preenchidos).
- **Fora do escopo desta mudança**: Recuperação de senha por e-mail/SMS (esqueci minha senha), login social (Google/Apple) e upload de foto de avatar.

## Capabilities

### New Capabilities
- `user-auth`: Registro, login, verificação de identidade e controle de perfil de acesso (`prestador` vs `cliente`) com autenticação baseada em JWT.

### Modified Capabilities
<!-- Nenhuma capacidade pré-existente foi modificada, pois esta é a primeira especificação do sistema. -->

## Impact

- **Backend (Xano)**: Criação/atualização da tabela `user` e ativação da API Group de autenticação (`/auth`).
- **Frontend (Streamlit)**: Atualização do fluxo em `app.py` para exibir formulários de login/cadastro e proteger áreas internas baseando-se no estado de autenticação.
- **Dependências**: Adição da biblioteca `requests` no ambiente Python para chamadas HTTP aos endpoints do Xano (se ainda não presente).
- **Variáveis de Ambiente**: Definição da variável `XANO_API_BASE_URL` em arquivo `.env` para apontar para a API do Xano.
