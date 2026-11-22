## Context

O AgendAí possui uma base sólida com Streamlit no frontend e Xano no backend, contando com autenticação JWT, catálogo de serviços, grade semanal de atendimento e motor anti-double-booking. Atualmente, a descoberta de profissionais depende de uma navegação manual pelo catálogo, a autenticação utiliza abas que concorrem no mesmo espaço visual e a interface necessita de refinamento estético unificado para transmitir a seriedade de um marketplace moderno de freelancers.

## Goals / Non-Goals

**Goals:**
- Implementar `services/recommendation_service.py` contendo o algoritmo de scoring multicritério normalizado (0 a 100), com cálculo determinístico baseado em pesos documentados.
- Aplicar filtros excludentes obrigatórios antes do ranking: profissionais sem disponibilidade na data ou com preço superior ao orçamento máximo são descartados sem gerar dados fictícios.
- Exibir justificativas claras dos fatores de recomendação em cada resultado.
- Separar completamente a tela de Login da tela de Cadastro no Streamlit sem o uso de abas, operando por navegação orientada a links e chave de estado `st.session_state["auth_page"]`.
- Adicionar validação de confirmação de senha no formulário de cadastro antes do envio ao backend Xano.
- Aplicar um design system moderno, profissional e consistente em 100% das páginas (sem poluição de emojis ou sombras excessivas).

**Non-Goals:**
- Não integrar chamadas pagas a APIs externas de LLMs (OpenAI/Anthropic) para o scoring; o algoritmo é determinístico, resiliente e baseado em regras matemáticas e correspondência textual.
- Não alterar as tabelas físicas do Xano de maneira destrutiva nem descartar os fluxos operacionais já aprovados de agendamento e disponibilidade.

## Decisions

- **Decisão 1: Algoritmo de Recomendação Multicritério em Python (`services/recommendation_service.py`)**:
  - *Fórmula*: Score Final = `(Compatibilidade * 0.35) + (Orçamento * 0.25) + (Disponibilidade * 0.25) + (Avaliação * 0.15)`
  - *Compatibilidade (0-100)*: Similaridade de palavras-chave entre a necessidade informada e os títulos/descrições dos serviços cadastrados.
  - *Orçamento (0-100)*: Relação percentual entre o preço do serviço e o teto do cliente (quanto mais econômico dentro do limite, maior a pontuação).
  - *Disponibilidade (0-100)*: Proporção de slots livres no expediente do prestador para a data solicitada (baseada no motor `calculate_available_slots`).
  - *Avaliação (0-100)*: Normalização da nota do prestador (padrão 5.0 estrelas = 100 pontos).
- **Decisão 2: Desacoplamento da Autenticação via Chave de Estado (`auth_page`)**:
  - Em vez de abas concorrentes, o estado `st.session_state["auth_page"]` define se o usuário vê a página de "login" ou a página de "signup".
  - Na página de Login, o link *"Não tem uma conta? Criar conta"* altera o estado para "signup" e invoca `st.rerun()`.
  - Na página de Cadastro, o link *"Já tem uma conta? Entrar"* redefine o estado para "login" e invoca `st.rerun()`.
  - O cadastro ganha campo de Confirmação de Senha validado localmente no frontend antes da chamada ao endpoint `auth/signup` do Xano.
- **Decisão 3: Design System Consistente e Centralizado**:
  - Definição de tokens de design em `.streamlit/config.toml` e componentes auxiliares em `services/ui_utils.py`.
  - Cartões de serviços e profissionais com tipografia hierárquica, paleta escura sóbria (`#0B0F19` base, `#111827` containers, `#3B82F6` destaque e `#10B981` status), botões de ação com contraste acessível e badges sutis.

## Risks / Trade-offs

- **[Risco] Cliente informa critérios muito restritivos (orçamento muito baixo ou data sem vagas)**:
  - *Mitigação*: Implementar estado vazio informativo e encorajador, explicando exatamente qual filtro limitou a busca e sugerindo aumentar o orçamento ou selecionar outra data.
- **[Risco] Navegação direta ou recarregamento acidental do navegador resetar a tela de cadastro**:
  - *Mitigação*: Persistir `st.session_state["auth_page"]` e fornecer link direto sempre visível de retorno ao Login.
