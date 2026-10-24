# Changelog — AgendAí

Todas as alterações notáveis deste projeto serão documentadas neste arquivo seguindo o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e versionamento semântico.

---

## [Unreleased] - 2026-10-24

### Adicionado (feat / ui)
- **Fechamento Operacional e Exportação (`arquivamento-mudancas-2026-10-24`)**:
  - Exportação da lista de atendimentos filtrados em formato CSV (UTF-8 com BOM e colunas em português) via `st.download_button` no painel do prestador.
  - Ação rápida de confirmação e lembrete com mensagem pré-formatada via WhatsApp (`https://wa.me/...`) nos cards de atendimento da agenda.
  - Associação de nome e telefone do cliente no fluxo de criação de agendamento em `services/appointment_service.py`.

---

## [0.3.0] - 2026-10-18

### Adicionado (feat / ui)
- **Refatoração Completa do Painel do Prestador (`app.py` & `services/ui_utils.py`)**:
  - Utilitários de formatação pt-BR para moeda brasileira (`R$ XX,XX`), datas por extenso e badges de status.
  - Saudação personalizada no cabeçalho com nome do usuário e data de hoje formatada.
  - Cartões de métricas neutros na aba Resumo (sem setas positivas quando valor for 0).
  - Listagem dos atendimentos do dia com estado vazio amigável e encorajador.
  - Agenda com filtros combinados de status e data, além de ações de confirmação e conclusão.
  - Gestão de serviços com visual em cards e formulários com feedback em toasts.
  - Nova especificação ativa consolidada: `openspec/specs/prestador-dashboard/spec.md`.

### Modificado (chore / db)
- **Limpeza de Dados e Alinhamento no Xano (`2026-10-18-limpeza-de-dados-xano`)**:
  - Backup das tabelas e expurgo de dados de testes antigos.
  - Padronização do usuário prestador Hector Barros no Xano.
  - Sincronização dos arquivos `.xs` do Xano no repositório.
- **Arquivamento OpenSpec**:
  - `openspec/changes/archive/2026-10-18-melhoria-ui-painel-prestador`
  - `openspec/changes/archive/2026-10-18-limpeza-de-dados-xano`

---

## [0.2.0] - 2026-10-13

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
