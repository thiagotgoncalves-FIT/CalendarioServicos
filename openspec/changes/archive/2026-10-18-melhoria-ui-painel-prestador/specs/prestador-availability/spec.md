## ADDED Requirements

### Requirement: Interface Ergonômica de Configuração da Grade
O sistema DEVE prover na aba Grade de Atendimento uma visualização intuitiva e organizada por dia da semana, com seletores claros de ativação do dia, campos de horário de início, término e pausa configuráveis, validações em tempo real e mensagem de sucesso ao salvar via toast/notificação.

#### Scenario: Salvamento com Feedback Visual da Grade
- **WHEN** o prestador clica no botão "Salvar Grade de Atendimento" com horários válidos
- **THEN** o sistema salva as alterações e exibe mensagem de confirmação sem recarregar desnecessariamente outros dados
