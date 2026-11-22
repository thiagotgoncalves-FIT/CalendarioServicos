## Why

O envio de e-mails via SMTP depende de credenciais de terceiros e serviços externos de entrega que podem falhar ou demorar para chegar na caixa postal.
Conforme solicitado pelo usuário, a recuperação de senha deve **voltar ao modelo auto-contido e imediato no próprio app**:
1. O usuário informa seu e-mail cadastrado.
2. O sistema valida a solicitação e **exibe o código de confirmação aleatório diretamente na tela do app**.
3. O usuário digita o código exibido para confirmar a intenção de recuperação.
4. O app autoriza o usuário a cadastrar uma nova senha, persistindo-a no sistema e permitindo o login imediato com a nova credencial, sem necessidade de envio por e-mail externo.

## What Changes

- **Exibição do Código de Confirmação Diretamente no App**:
  - Na etapa 2 da recuperação de senha, renderizar visualmente a caixa com o código de 6 dígitos gerado.
  - Eliminar a obrigatoriedade de envio via SMTP/e-mail externo.
- **Validação e Redefinição Imediata**:
  - O usuário digita o código exibido e o sistema valida a correspondência.
  - Ao validar o código com sucesso, o app libera o formulário para criação da Nova Senha e Confirmação.
  - A nova senha é salva de forma persistente em `uploads/user_credentials.json` e na base de dados de autenticação.

## Capabilities

### Modified Capabilities
- `user-profile`: Apresentar o código de verificação para redefinição de senha diretamente na interface gráfica da aplicação, simplificando o processo de recuperação e dispensando o envio de e-mails externos.

## Impact

- **Código Afetado**: `app.py` (restauração da caixa visual com o código de confirmação), `services/auth_service.py` (simplificação sem bloqueio por SMTP).
- **APIs / Dados**: Persistência mantida em `uploads/user_credentials.json`.
