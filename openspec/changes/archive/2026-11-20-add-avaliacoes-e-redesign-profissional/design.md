# Technical Design: add-avaliacoes-e-redesign-profissional

## Context

A plataforma AgendAí é construída em Streamlit no frontend e consome endpoints REST do backend Xano (com camada de resiliência e fallback em memória caso a API esteja em modo local ou indisponível). O modelo de dados de agendamento suporta o ciclo de vida (`pendente` ➔ `confirmado` ➔ `concluido` / `cancelado`). Atualmente, o frontend exibe informações técnicas do ambiente de desenvolvimento (endereços de backend, termos de resiliência e metadados de laboratório acadêmico), além de não possuir entidade ou interface para registrar e consultar avaliações dos atendimentos concluídos.

## Goals / Non-Goals

**Goals:**
- Prover um módulo de serviço `services/review_service.py` padronizado com funções de submissão, listagem, cálculo de nota média agregada e verificação de elegibilidade de avaliação por atendimento.
- Integrar a camada de resiliência com fallback para avaliações, permitindo operação completa e testes autônomos sem dependência forçada de migrações manuais síncronas de banco.
- Exibir a nova aba pública "Avaliações" com nota média, número total de feedbacks e cards de depoimentos com nome de exibição seguro (ex: "Lucas F.") e ordenação recente.
- Incorporar o botão e formulário de avaliação nos cards de atendimentos concluídos na aba "Meus Agendamentos", com controle estrito contra reavaliações.
- Realizar varredura e saneamento completo de todos os textos, badges e modais na aplicação, removendo termos como "Xano", "API", "Camada de Resiliência", "Innovation Lab", IDs de entidades internas e mensagens técnicas.

**Non-Goals:**
- Criação de fluxo complexo de denúncia/moderação administrativa (a publicação é direta, com validação de entrada de 1 a 5 estrelas e limite de caracteres).
- Resposta pública do prestador ao comentário do cliente (fora do escopo deste ciclo).
- Migração de framework ou introdução de bibliotecas não-Streamlit no frontend.

## Decisions

### 1. Modelo de Dados da Avaliação (`Review`)
- **Decisão**: A entidade de avaliação conterá: `id`, `agendamento_id` (chave de unicidade 1:1), `cliente_id`, `prestador_id`, `cliente_nome_exibicao`, `nota` (inteiro de 1 a 5), `comentario` (string até 500 caracteres) e `criado_em` (data/hora ISO).
- **Justificativa**: Permite rastrear com precisão o atendimento avaliado, assegura que o prestador e o cliente estejam associados e viabiliza a exibição pública do nome sem expor dados pessoais completos.
- **Alternativas consideradas**:
  - *Avaliação solta sem vínculo a agendamento*: Rejeitada por abrir brecha para avaliações falsas ou spam.
  - *Avaliação direta no prestador*: Rejeitada porque a avaliação deve refletir a experiência de um serviço específico realizado.

### 2. Exibição da Identidade do Cliente (Privacidade e Humanização)
- **Decisão**: Exibir o primeiro nome e a inicial do último sobrenome (ex.: "Mariana S.", "Lucas F.").
- **Justificativa**: Equilibra credibilidade e transparência pública para quem lê com privacidade para o cliente final.
- **Alternativas consideradas**:
  - *Exibição de nome completo com e-mail*: Inaceitável por violação de privacidade.
  - *Anonimato total*: Reduz a credibilidade dos depoimentos para novos clientes.

### 3. Ponto de Acesso à Avaliação: Aba "Meus Agendamentos"
- **Decisão**: O formulário de avaliação será embutido diretamente no card de cada atendimento com status `concluido` na aba do cliente.
- **Justificativa**: O cliente já utiliza essa aba para consultar seu histórico. Uma vez que o prestador conclui o atendimento, o status muda para `concluido` e a interface apresenta imediatamente o botão "Avaliar Atendimento". Ao enviar, o card é atualizado com um badge "Avaliado ★★★★★" e o formulário é desabilitado.
- **Alternativas consideradas**:
  - *Envio de link externo por e-mail/WhatsApp*: Aumentaria a dependência de serviços externos de mensageria não configurados e tokens temporários complexos.

### 4. Remoção de Termos Técnicos e Saneamento Visual
- **Decisão**: Na barra lateral, remover o subtítulo acadêmico e o expander "Conexão e Status". Nas mensagens de toast e alerts, substituir mensagens como "Criando sua conta com segurança no Xano..." por "Criando sua conta...". Nos cards, ocultar "Agendamento #ID" e "Cliente #ID", exibindo apenas o nome do profissional/cliente e do serviço.
- **Justificativa**: O produto passa a ter identidade 100% voltada ao consumidor, limpa e profissional.

## Risks / Trade-offs

- **[Risco] Reavaliação acidental ou concorrência**: Cliente clicar repetidamente no botão de envio.
  - *Mitigação*: Verificação em memória e em backend de `is_appointment_reviewed(agendamento_id)` antes de gravar, com desativação do formulário após submissão bem-sucedida.
- **[Risco] Atendimentos legados sem avaliação**: Clientes antigos podem ter agendamentos concluídos sem avaliação.
  - *Mitigação*: O sistema lida graciosamente com atendimentos concluídos não avaliados, exibindo o convite para avaliar apenas se o cliente desejar.
- **[Risco] Ausência de avaliações no primeiro acesso**: A aba pública de avaliações ficar vazia inicialmente.
  - *Mitigação*: Estado vazio acolhedor com ilustração amigável e texto explicativo, sem erros matemáticos de divisão por zero no cálculo da média.

