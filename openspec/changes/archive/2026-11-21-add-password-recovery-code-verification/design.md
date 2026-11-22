## Context

O usuário solicitou: *"volte para quando estava mostrando o código na tela, não precisa mais enviar por email"*.

O fluxo de exibição do código diretamente no aplicativo torna o sistema 100% autônomo, sem bloqueios de rede, sem risco de falha de entrega de e-mail e sem exigir credenciais SMTP ou contas de terceiros.

## Goals / Non-Goals

**Goals:**
- Restaurar a caixa visual em `app.py` que apresenta o código de 6 dígitos gerado para o usuário na Etapa 2.
- Permitir que o usuário digite o código de 6 dígitos exibido para liberar a troca de senha.
- Não depender de envio de e-mail externo.
- Persistir a nova senha em `uploads/user_credentials.json` para que o login funcione imediatamente com a nova credencial.

**Non-Goals:**
- Não manter bloqueio ou dependência de provedores de SMTP no fluxo de recuperação.

## Decisions

1. **Exibição Visual do Código no App (`app.py`)**:
   - Na Etapa 2 da recuperação de senha, restaurar o container com destaque visual:
     ```html
     <div style="background:#EFF6FF; border:1px solid #BFDBFE; ...">
       <div>Seu Código de Confirmação</div>
       <div style="font-size:2.2rem; ...">{rec_code}</div>
     </div>
     ```
2. **Desacoplamento de SMTP**:
   - O avanço para a etapa do código é instantâneo, sem esperar resposta de servidores de e-mail externos.
3. **Persistência Imediata da Nova Senha**:
   - Ao confirmar a nova senha na Etapa 3, salvar no arquivo permanente `uploads/user_credentials.json`.
