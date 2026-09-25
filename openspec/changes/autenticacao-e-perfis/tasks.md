## 1. Dependências e Configuração de Ambiente

- [x] 1.1 Adicionar bibliotecas `requests` e `python-dotenv` ao `requirements.txt` e verificar que a instalação no `.venv` é concluída sem conflitos.
- [x] 1.2 Criar arquivo `.env.example` documentando a variável `XANO_API_URL` e verificar sua presença no repositório.

## 2. Camada de Serviços e Integração HTTP

- [x] 2.1 Criar módulo `services/api_client.py` com carregamento de variáveis de ambiente e métodos genéricos para requisições GET e POST com tratamento de exceções de conexão.
- [x] 2.2 Criar módulo `services/auth_service.py` implementando as funções `signup`, `login` e `get_current_user` com validação de payload.

## 3. Interface de Autenticação e Perfis no Streamlit

- [x] 3.1 Construir tela de autenticação em `app.py` com abas para "Entrar" (Login) e "Criar Conta" (Cadastro), incluindo seleção explícita de perfil (`prestador` ou `cliente`).
- [x] 3.2 Integrar gerenciamento de sessão com `st.session_state` para armazenar `authenticated`, `auth_token` e dados do `user`.
- [x] 3.3 Implementar exibição condicional do dashboard inicial personalizado de acordo com o perfil logado e botão de "Encerrar Sessão" (Logout).

## 4. Validação e Testes Integrados

- [x] 4.1 Executar teste funcional local da interface Streamlit e verificar respostas visuais de sucesso e mensagens de erro (campos obrigatórios e falha de login).
- [x] 4.2 Executar validação formal da especificação no OpenSpec (`openspec validate autenticacao-e-perfis`) e verificar aprovação com status zero-errors.
