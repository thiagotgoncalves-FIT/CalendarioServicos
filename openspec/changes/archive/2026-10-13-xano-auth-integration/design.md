## Context

O API Group `Authentication` no Xano (canonical `M19UcCw4`) já existe e os endpoints `/auth/signup`, `/auth/login` e `/auth/me` estão publicados. O problema é que o Function Stack de todos eles está vazio — sem inputs, sem lógica, sem response — causando retorno `null` para toda chamada e ativando sempre o fallback em memória no Python.

A tabela `user` já está modelada corretamente com campo `password` do tipo `password` (hash automático pelo Xano, validação de mínimo 8 chars, 1 letra, 1 dígito) e índice único em `email`. O schema está correto e não precisa ser recriado.

A URL base da API no `.env` (`https://x8ki-letl-twmt.n7.xano.io/api:M19UcCw4`) aponta corretamente para o API Group `Authentication`.

## Goals / Non-Goals

**Goals:**
- Implementar o Function Stack dos endpoints `signup_POST.xs`, `login_POST.xs` e `me_GET.xs` usando XanoScript e publicar via `xano workspace push`.
- Alterar o `enum role` em `table/user.xs` de `["admin", "member"]` para `["prestador", "cliente"]`.
- Ajustar `auth_service.py` para não acionar fallback quando o Xano retornar erro real de negócio (ex.: email duplicado, credenciais erradas).
- Alinhar validação de senha mínima no frontend: 8 chars com 1 letra e 1 dígito.

**Non-Goals:**
- Não implementar reset de senha ou magic link neste ciclo.
- Não alterar a URL do API Group ou criar novos API Groups.
- Não migrar dados (não há dados reais gravados ainda).

## Decisions

### Decisão 1: Implementar via Xano CLI (`workspace push`)
**Escolha**: editar os arquivos `.xs` localmente e publicar com `xano workspace push`.
**Alternativa**: editar manualmente no dashboard web do Xano.
**Rationale**: Manter o fluxo code-as-infrastructure alinhado com o OpenSpec. O CLI garante rastreabilidade via Git dos arquivos `.xs`.

### Decisão 2: Function Stack do `signup` — usar `Create Record` nativo do Xano
**Escolha**: usar o statement nativo de `createRecord` na tabela `user`. O Xano aplica automaticamente o hash da senha porque o campo é do tipo `password`.
**Alternativa**: hash manual com `bcrypt` via custom function.
**Rationale**: O mecanismo nativo do Xano já implementa a política de senha (mínimo 8 chars, 1 letra, 1 dígito) e o hash de forma segura. Não duplicar responsabilidade.

### Decisão 3: Function Stack do `login` — usar `getAuthToken` com `checkPassword` nativo
**Escolha**: usar o statement nativo `get auth token` do Xano que realiza lookup por email e verifica o hash da senha automaticamente.
**Rationale**: O Xano expõe exatamente esse mecanismo para login com tabela de `auth = true`. É a abordagem padrão documentada.

### Decisão 4: enum `role` — alterar para domínio do projeto
**Escolha**: mudar `["admin", "member"]` para `["prestador", "cliente"]` diretamente no `user.xs`.
**Alternativa**: mapeamento Python (admin↔prestador, member↔cliente).
**Rationale**: Sem dados reais gravados e os outros endpoints (`agenda`, `members_accounts`) do workspace são do template Xano Quick Start e não fazem parte do escopo do AgendAí. A mudança evita confusão conceitual e não há risco de regressão.

### Decisão 5: Fallback resiliente — manter mas restringir
**Escolha**: manter o fallback para erros de infraestrutura (timeout, 5xx) mas desativá-lo para respostas `null` com HTTP 200, que agora indicarão erro de configuração do Xano (não indisponibilidade).
**Rationale**: Após a implantação, um `200 null` não deve ser confundido com indisponibilidade. Os endpoints reais retornarão dados ou erro HTTP com body.

## Risks / Trade-offs

- **Risco: enum `role` quebra template Xano** → Os outros API Groups (`members_accounts`, `event_logs`) do workspace são exemplos do Quick Start e não são consumidos pelo AgendAí. Mitigação: verificar os endpoints de `members_accounts` antes do push para confirmar que não referenciam `role = "admin"` de forma hardcoded.
- **Risco: `workspace push` sobrescrever lógica existente** → Os stacks estão vazios; o push só adiciona lógica nova. Mitigação: fazer pull antes do push para confirmar estado atual.
- **Trade-off: fallback desativado para `200 null`** → Se um endpoint não-relacionado retornar `null` legitimamente, pode causar erro. Aceitável para o escopo atual onde todos os endpoints retornam dados reais.

## Migration Plan

1. Pull do workspace para garantir estado mais recente.
2. Editar `table/user.xs` (enum role).
3. Implementar stacks dos 3 endpoints `.xs`.
4. Push via `xano workspace push`.
5. Teste end-to-end: signup novo usuário → login → `/auth/me`.
6. Ajustar `auth_service.py` e validação de senha mínima no frontend.
7. Validar que mock fallback não é acionado em nenhum dos fluxos de sucesso.
