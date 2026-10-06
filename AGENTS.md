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

**Regra absoluta**: Nenhuma funcionalidade nova pode ser implementada sem passar pelo ciclo completo abaixo. A IA propõe — o grupo decide — a IA implementa.

```
CONTEXTO GLOBAL (AGENTS.md + project-overview.md + domain-model.md + config.yaml)
        |
        v
[1] /opsx-explore
     Investigar o problema, mapear dependencias, entender o codigo existente.
     NAO implementa codigo. NAO cria change ainda.
     Resultado: clareza sobre o que sera feito.
        |
        v
[2] /opsx-propose
     Gera os artefatos da change:
       proposal.md   -> Por que? O que muda? Escopo.
       specs/        -> Comportamento esperado e verificavel.
       design.md     -> Como sera implementado tecnicamente.
       tasks.md      -> Checklist de tarefas pequenas e verificaveis.
        |
        v
[3] REVIEW (obrigatorio pelo grupo)
     proposal.md : problema claro? escopo adequado?
     spec.md     : comportamento correto? casos de erro cobertos?
     design.md   : solucao tecnica faz sentido com a arquitetura?
     tasks.md    : tasks pequenas? todas necessarias e verificaveis?
     --> Sem aprovacao humana explicita, NAO avancar para Apply.
        |
        v
[4] /opsx-apply
     Implementa seguindo tasks.md como checklist.
     Marca [x] conforme cada tarefa e concluida.
     Interrompe e consulta o grupo se surgir:
       - decisao que contradiga o dominio;
       - alteracao arquitetural significativa;
       - escopo nao previsto.
        |
        v
[5] /opsx-archive
     Consolida a especificacao em openspec/specs/
     Move a change concluida para openspec/changes/archive/
        |
        v
  PROXIMA CHANGE -> voltar ao passo [1]
```

### Princípios do ciclo
- **Vertical**: cada Change entrega backend + frontend integrados — nunca apenas banco ou apenas tela.
- **Incremental**: uma funcionalidade por vez; nunca construir tudo de uma só vez.
- **DB acompanha a feature**: a modelagem física no Xano evolui junto com as funcionalidades, não é criada toda de uma vez.
- **Revisão humana é obrigatória**: a saída da IA não é automaticamente correta. O grupo analisa, aprova ou corrige antes de avançar.
- **`config.yaml` context vs `spec`**: o `context` contém apenas o que se aplica a praticamente todas as changes; detalhes específicos de uma funcionalidade vão na respectiva `spec`.

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
