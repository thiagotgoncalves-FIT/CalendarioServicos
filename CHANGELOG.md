# Changelog — AgendAí

Todas as alterações notáveis deste projeto serão documentadas neste arquivo seguindo o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e versionamento semântico.

---

## [Unreleased] - 2026-10-13

### Adicionado (feat)
- **Integração Real de Autenticação com o Xano**:
  - Implementação dos Function Stacks de `auth/signup`, `auth/login` e `auth/me` no Xano via XanoScript e deploy pelo Xano CLI (`@xano/cli`).
  - Gravação de senhas com hash criptográfico nativo do Xano (campo `password`) e validação via `security.check_password`.
  - Atualização do schema da tabela `user` com os perfis de acesso oficiais (`["prestador", "cliente"]`) e campo de contato `phone`.
  - Emissão de tokens seguros JWE/JWT para gerenciamento de sessão de usuário.
- **Motor de Cálculo de Horários Livres e Agendamento**:
  - Algoritmo de cálculo de slots disponíveis em intervalos de 30 minutos em `services/appointment_service.py`.
  - Validação estrita de expediente, pausa para almoço, horários passados e prevenção atômica contra sobreposição de reservas (*anti-double-booking*).
  - Fluxo completo de agendamento na interface do cliente com seleção interativa de data e seletor de horários.
  - Painel do prestador com listagem de atendimentos, filtros de status e botões de ação rápida (Confirmar, Concluir, Cancelar).
- **Interface Dark Theme Premium**:
  - Estilização completa do Streamlit em Dark Theme profissional (`.streamlit/config.toml` e CSS customizado com glassmorphism).

### Modificado (refactor / fix)
- **Serviço de Autenticação (`services/auth_service.py`)**:
  - Alinhamento da validação de senha para o critério do Xano (mínimo de 8 caracteres, com letra e número).
  - Remoção de fallback que mascarava respostas legítimas de erro da API (e-mail duplicado com 400 ou credenciais incorretas com 403 passam a exibir mensagens amigáveis na interface).
  - Normalização da resposta de `get_current_user` para suporte transparente entre Streamlit e a API do Xano.
- **Cliente HTTP (`services/api_client.py`)**:
  - Tratamento aprimorado de status codes e cabeçalhos de autorização Bearer Token.

### Especificação & Metodologia (docs / chore)
- Conclusão e arquivamento das changes via OpenSpec:
  - `2026-10-13-dark-theme-auth-resilience`
  - `2026-10-13-xano-auth-integration`
  - `2026-10-13-motor-de-agendamento`
- Consolidação e validação de 100% das specs ativas:
  - `specs/appointment-engine`
  - `specs/user-auth`
  - `specs/service-catalog`
  - `specs/prestador-availability`
