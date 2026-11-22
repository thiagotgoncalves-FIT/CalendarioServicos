## 1. Eliminação do Botão de Voltar Redundante no Topo

- [x] 1.1 Em `app.py`, ajustar a barra superior para não renderizar o botão "⬅️ Voltar ao Painel" quando `is_settings` for verdadeiro, deixando a ação de retorno unificada no cabeçalho de `render_account_settings_view`.
- [x] 1.2 Garantir que o botão "⚙️ Configurações" continue disponível quando o usuário estiver no painel principal.

## 2. Testes e Validação

- [x] 2.1 Executar os testes automatizados da plataforma (`test_user_settings.py`, `test_appointment_engine.py`).
- [x] 2.2 Validar a especificação estrita do OpenSpec com `openspec validate add-botao-retorno-dashboard --strict`.
