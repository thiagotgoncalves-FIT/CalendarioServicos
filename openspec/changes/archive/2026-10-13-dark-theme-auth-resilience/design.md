## Context

A arquitetura do AgendAí prevê o Streamlit como frontend consumindo APIs REST do Xano. No entanto, se o endpoint de autenticação do Xano (`/auth/signup`) estiver retornando corpo `null` (por ausência de lógica no Function Stack remoto) ou se houver instabilidade de rede, o usuário não pode ficar bloqueado de testar as telas de prestador e cliente. Além disso, a estética visual atual carece de identidade moderna, demandando um Dark Theme refinado.

Consulte [proposal.md](proposal.md) para a motivação detalhada e [specs/user-auth/spec.md](specs/user-auth/spec.md) para os critérios de aceitação.

## Goals / Non-Goals

**Goals:**
- Implementar estratégia de tolerância a falhas em `auth_service.py` (tenta a chamada ao Xano; se retornar nulo, vazio ou código de erro de infraestrutura, registra o usuário na sessão/memória local e permite navegação imediata).
- Garantir que a criação de novo usuário e login funcionem perfeitamente para os perfis `prestador` e `cliente`.
- Configurar o tema escuro profissional em `.streamlit/config.toml` e estilizar componentes (cards, inputs, badges, botões) via CSS customizado em `app.py`.
- Apresentar status claro de conectividade na barra lateral informando se a sessão está operando via Xano ou modo de resiliência.

**Non-Goals:**
- Não alterar as regras de negócio de agendamento ou catálogo de serviços.
- Não remover os endpoints nem a URL do Xano configurada no `.env` (mantendo-a como prioridade 1 para chamadas REST).

## Decisions

### Decisão 1: Fallback Inteligente de Autenticação em Duas Etapas
- **Abordagem**:
  1. O método `signup()` e `login()` faz POST para o endpoint real do Xano.
  2. Se a resposta for bem-sucedida E contiver `authToken` válido com payload de usuário, utiliza a resposta do Xano diretamente.
  3. Se a resposta for `null` (HTTP 200 com corpo vazio), status 503 ou erro de rede, o serviço registra o novo usuário no repositório de memória em tempo de execução (`_MOCK_USERS_DB`), emite um token de sessão e autoriza o acesso.
- **Alternativa Descartada**: Bloquear a aplicação e exigir que o usuário reconfigure manualmente o Function Stack no painel web do Xano antes de poder testar ou usar o frontend.

### Decisão 2: Dark Theme Baseado em Tokens de Cores Modernos
- **Abordagem**:
  - Background principal: `#0B0F19` (Obsidian Dark) no `.streamlit/config.toml` e `#0F172A` (Slate 900) para cards.
  - Cartões com efeito suave de profundidade e bordas sutis `rgba(255, 255, 255, 0.08)`.
  - Destaque interativo com foco azul elétrico (`#3B82F6` / `#2563EB`) nos campos de formulário e botões de ação primária.
  - Tipografia nítida com títulos `#F8FAFC` e textos secundários `#94A3B8`.
- **Alternativa Descartada**: Depender exclusivamente do tema dark nativo do Streamlit sem CSS customizado, o que geraria contraste insuficiente em formulários e botões genéricos.

## Risks / Trade-offs

- **[Dados em memória no fallback]** → Caso a aplicação seja reiniciada e o Xano continue retornando `null`, os usuários criados no fallback em memória serão resetados. *Mitigação*: Os usuários padrão pré-configurados (`carlos@barbearia.com`, `mariana@email.com`) continuam sempre disponíveis para teste imediato.
- **[Conflito de estilos CSS do Streamlit]** → Seletores de classe internos do Streamlit podem variar entre versões. *Mitigação*: Utilizar seletores baseados em atributos (`div[data-testid="stForm"]`, `.stTextInput input`) e variáveis nativas do tema.
