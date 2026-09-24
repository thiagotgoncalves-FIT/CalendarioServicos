# Instruções para Agentes de IA (AGENTS.md)

Este documento estabelece as regras operacionais para qualquer agente de Inteligência Artificial trabalhando neste projeto no ambiente **Antigravity**.

---

## 1. Documentação e Contexto
- Antes de propor ou realizar alterações significativas, consulte sempre os documentos de contexto:
  - [`docs/project-overview.md`](docs/project-overview.md)
  - [`docs/domain-model.md`](docs/domain-model.md)
  - [`openspec/config.yaml`](openspec/config.yaml)
- Mantenha esses documentos estáveis. Se uma regra pertencer a uma funcionalidade específica, registre-a na respectiva `spec` da mudança, e não no contexto global.

---

## 2. Frontend (Streamlit)
- O frontend do projeto deve ser implementado **exclusivamente com Streamlit**.
- Não introduza React, Vue, Angular, Next.js ou qualquer outra tecnologia de frontend para substituir ou complementar o Streamlit, salvo quando houver uma alteração arquitetural explicitamente aprovada para o projeto.
- Organize o código em `app.py` e, caso surjam múltiplas páginas, siga a estrutura nativa de páginas do Streamlit (`pages/`).
- Utilize componentes visuais modernos, gerenciamento de estado via `st.session_state` e tratamento adequado de exceções.

---

## 3. Backend e XanoScript (Xano)
- O backend e a persistência de dados pertencem exclusivamente ao **Xano**.
- Toda a comunicação entre o frontend Streamlit e o backend é realizada por meio de APIs REST.
- Ao trabalhar com XanoScript (`.xs`), utilize as ferramentas do **Xano Developer MCP** configuradas no ambiente para:
  - Consultar documentação oficial de sintaxe;
  - Validar arquivos e lógica do XanoScript;
  - Não presuma nem invente comandos ou sintaxes sem validação prévia.
- Arquivos locais sincronizados do workspace Xano residem na pasta `xano/`.

---

## 4. Metodologia de Desenvolvimento (OpenSpec)
- Todas as alterações funcionais e técnicas relevantes devem seguir rigorosamente o fluxo **Spec-Driven Development (SDD)** do OpenSpec:
  1. `/opsx-explore`: Mapeamento de terreno e investigação conceitual (não gera código nem altera o banco).
  2. `/opsx-propose`: Geração estruturada de artefatos (`proposal.md`, `specs/`, `design.md`, `tasks.md`).
  3. **Revisão Humana**: Aguarde a validação do usuário antes de codificar.
  4. `/opsx-apply`: Implementação guiada estritamente pelo checklist de `tasks.md`, marcando as tarefas à medida que forem concluídas.
  5. `/opsx-archive`: Consolidação da especificação permanente em `openspec/specs/` e arquivamento do histórico.
- Nunca tente construir todo o sistema de uma vez; decomponha o desenvolvimento em mudanças incrementais e verificáveis.

---

## 5. Código e Qualidade
- Reutilize código existente sempre que apropriado e evite duplicações.
- Não modifique arquivos ou funcionalidades fora do escopo da mudança atual sem justificativa explícita.
- Mantenha `requirements.txt` atualizado caso novas bibliotecas essenciais sejam adicionadas.

---

## 6. Segurança
- Regras críticas de validação de dados, autorização e integridade devem residir no backend (Xano).
- O frontend não é um mecanismo seguro de proteção de dados.
- Nunca adicione tokens de API, chaves secretas ou credenciais diretamente no código ou em arquivos versionados. Utilize `.env` (ignorado pelo `.gitignore`).

---

## 7. Versionamento com Git
- Verifique sempre o estado do repositório com `git status` e `git diff` antes e após alterações importantes.
- Nunca versione a pasta do ambiente virtual (`.venv/`) ou arquivos temporários.
- Utilize mensagens de commit semânticas e claras (ex.: `feat: ...`, `fix: ...`, `docs: ...`).
