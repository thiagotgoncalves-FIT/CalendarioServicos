## ADDED Requirements

### Requirement: Recuperação de Senha com Exibição de Código no App
O sistema MUST exibir o código numérico de 6 dígitos de verificação diretamente na interface gráfica da aplicação ao solicitar a recuperação de senha, permitindo ao usuário confirmar o código e cadastrar sua nova senha sem dependência de envio de e-mails externos.

#### Scenario: Geração e Apresentação do Código na Tela
- **GIVEN** que o usuário informa seu e-mail na tela de recuperação de senha
- **WHEN** o usuário solicita a redefinição de senha
- **THEN** o sistema gera o código de 6 dígitos e o exibe com destaque na tela do aplicativo com campo para digitação e conferência

#### Scenario: Redefinição de Senha Bem-Sucedida
- **GIVEN** que o código de 6 dígitos está exibido na tela
- **WHEN** o usuário insere o código exibido e cadastra uma nova senha válida
- **THEN** o sistema atualiza a senha permanentemente e libera o acesso com a nova credencial
