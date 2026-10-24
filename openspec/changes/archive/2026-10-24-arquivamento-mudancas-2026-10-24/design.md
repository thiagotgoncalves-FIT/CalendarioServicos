## Context

O painel do prestador já conta com a listagem dinâmica de atendimentos na aba "Agenda de Atendimentos", com filtros de data e status. Para a entrega final, é necessário permitir a exportação desse relatório para conciliação financeira do prestador e fornecer um canal rápido de contato e confirmação com o cliente via WhatsApp diretamente pelo card do agendamento, além de formalizar o arquivamento das mudanças no repositório Git.

## Goals / Non-Goals

**Goals:**
- Implementar gerador de CSV em memória (`io.StringIO`) nos utilitários visuais/de serviço (`services/ui_utils.py`), sem necessidade de bibliotecas externas pesadas.
- Integrar `st.download_button` no topo da lista de atendimentos na aba "Agenda de Atendimentos" em `app.py`.
- Formatar links diretos para WhatsApp (`https://wa.me/55...`) com sanitização de dígitos numéricos e mensagem codificada via `urllib.parse.quote`.
- Atualizar a documentação final (`README.md` e `CHANGELOG.md`) e preparar o commit no padrão Conventional Commits.

**Non-Goals:**
- Não implementar disparador automático via API oficial paga do WhatsApp Business (ex: Twilio ou Meta Cloud API); a comunicação ocorre via link `wa.me` acionado manualmente pelo usuário no navegador.
- Não alterar a modelagem física do banco de dados no Xano.

## Decisions

- **Decisão 1: Geração de CSV em Memória via `io.StringIO`**:
  - *Alternativa considerada*: Gerar arquivo físico temporário em disco.
  - *Razão*: Geração em memória é mais segura, limpa e perfeitamente compatível com o componente nativo `st.download_button` do Streamlit.
- **Decisão 2: Formatação de Lembrete no WhatsApp**:
  - *Alternativa considerada*: Apenas exibir o número de telefone como texto estático.
  - *Razão*: O link dinâmico com mensagem pré-preenchida ("Olá [Cliente]! Confirmando seu agendamento de [Serviço] no AgendAí para [Data] às [Hora]...") reduz o atrito e resolve a dor de *no-show*.
- **Decisão 3: Sanitização de Telefones**:
  - Garantir que apenas caracteres numéricos sejam passados no link do WhatsApp, adicionando DDI 55 caso o número tenha DDD padrão brasileiro.

## Risks / Trade-offs

- **[Risco] Cliente sem telefone cadastrado ou formato inválido**:
  - *Mitigação*: Verificar presença de telefone e tamanho mínimo (10 ou 11 dígitos); se ausente, ocultar o botão de WhatsApp e exibir apenas o nome do cliente.
- **[Risco] Lista de atendimentos vazia no filtro**:
  - *Mitigação*: Desabilitar o botão de download de CSV com `disabled=True` e exibir mensagem informativa amigável.
