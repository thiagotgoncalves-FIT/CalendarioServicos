## Context

Ver `proposal.md` para a motivação de negócio e escopo.
O projeto utiliza **Xano** como backend exclusivo (banco de dados relacional e APIs REST) e **Streamlit** (Python 3.14) como frontend exclusivo. As decisões técnicas devem respeitar a integridade de dados e validação de segurança no backend, enquanto o frontend lida com a experiência do usuário e controle de sessão local.

## Goals / Non-Goals

**Goals:**
- Definir a modelagem física da tabela `user` no Xano com tipagem adequada e campos essenciais (`name`, `email`, `password`, `phone`, `role`).
- Padronizar os contratos de payload dos endpoints REST de autenticação (`POST /auth/signup`, `POST /auth/login` e `GET /auth/me`).
- Desenhar a camada de serviço no Streamlit (`services/auth_service.py`) para encapsular requisições HTTP e tratamento de exceções.
- Estruturar o gerenciamento de estado da sessão no Streamlit (`st.session_state`) para suportar alternância entre áreas autenticadas de Prestador e Cliente.

**Non-Goals:**
- Autenticação federada / OAuth2 (Google, Apple, Facebook).
- Armazenamento persistente de sessão via cookies de longa duração no navegador (manteremos em memória na sessão Streamlit para simplicidade do MVP).
- Recuperação de senha por e-mail com envio de tokens transacionais.

## Decisions

### 1. Utilização da Camada de Autenticação Nativa do Xano
- **Decisão**: Utilizar o gerador de autenticação nativo do Xano (Auth API Group), que já implementa criptografia de senha com bcrypt e geração de tokens JWT seguros.
- **Alternativa Considerada**: Criar endpoints manuais e implementar lógica de hash customizada. Foi descartada por adicionar complexidade desnecessária e aumentar o risco de falhas de segurança.

### 2. Segregação de Papel (`role`) via Campo Direto na Tabela `user`
- **Decisão**: Adicionar a coluna `role` (tipo text/enum com valores `'prestador'` ou `'cliente'`) diretamente na tabela `user`.
- **Alternativa Considerada**: Criar tabelas separadas (`prestador` e `cliente`) com relação 1:1. Foi descartada para o MVP, pois ambas as entidades compartilham credenciais, contato e ciclo de autenticação idênticos. O perfil direciona quais telas e dados são acessados.

### 3. Contratos de API REST

#### `POST /auth/signup`
- **Payload Request**:
  ```json
  {
    "name": "Nome Completo",
    "email": "usuario@exemplo.com",
    "password": "senha_segura",
    "phone": "11999999999",
    "role": "prestador"
  }
  ```
- **Response Success (200 OK)**:
  ```json
  {
    "authToken": "jwt_token_string",
    "user": {
      "id": 1,
      "name": "Nome Completo",
      "email": "usuario@exemplo.com",
      "phone": "11999999999",
      "role": "prestador"
    }
  }
  ```

#### `POST /auth/login`
- **Payload Request**:
  ```json
  {
    "email": "usuario@exemplo.com",
    "password": "senha_segura"
  }
  ```
- **Response Success (200 OK)**:
  ```json
  {
    "authToken": "jwt_token_string",
    "user": {
      "id": 1,
      "name": "Nome Completo",
      "email": "usuario@exemplo.com",
      "phone": "11999999999",
      "role": "prestador"
    }
  }
  ```

### 4. Camada de Integração no Frontend Streamlit
- **Decisão**: Criar o diretório `services/` com:
  - `services/api_client.py`: Centraliza a URL base da API (lida via variável de ambiente `XANO_API_URL` com fallback amigável) e métodos genéricos `post` e `get` com headers de autorização (`Authorization: Bearer <token>`).
  - `services/auth_service.py`: Expõe funções limpas `login(email, password)`, `signup(name, email, password, phone, role)` e `get_current_user(token)`.
- **Alternativa Considerada**: Fazer chamadas `requests.post` diretamente no corpo de `app.py`. Descartada para evitar código espaguete e facilitar testes de integração.

### 5. Gerenciamento de Estado no Streamlit
- **Decisão**: Utilizar `st.session_state` com as seguintes chaves padronizadas:
  - `st.session_state["authenticated"]`: booleano (`True` / `False`).
  - `st.session_state["auth_token"]`: string com o JWT ou `None`.
  - `st.session_state["user"]`: dicionário com os dados do usuário logado.

## Risks / Trade-offs

- **[Recarregar a página (F5) reinicia a sessão no Streamlit]** → **Mitigação**: Comportamento aceitável no estágio de MVP acadêmico. Como boa prática de UX, orientar o usuário e manter a interface de login com autopreenchimento rápido durante testes.
- **[Conexão com a API indisponível ou URL não configurada]** → **Mitigação**: O `api_client` captura erros de rede e exibe alerta amigável no Streamlit com instrução de conferir a variável `XANO_API_URL`.

## Migration Plan

1. Assegurar as dependências `requests` e `python-dotenv` no `requirements.txt`.
2. Criar arquivo de exemplo `.env.example` no repositório com a variável `XANO_API_URL=https://...`.
3. Sincronizar endpoints e tabelas criadas no Xano.
