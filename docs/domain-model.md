# Modelo de Domínio — Projeto Integrador

Este documento define os conceitos fundamentais do domínio da aplicação, suas responsabilidades, relacionamentos e regras estruturais essenciais. Ele serve para alinhar o entendimento conceitual antes das decisões locais de implementação.

---

## 1. Visão Geral das Entidades

```text
Usuario (Perfil / Auth)
  │
  ├── 1:N ── RegistroAtividade (Auditoria / Logs)
  │
  └── 1:N ── RecursoPrincipal (Entidade central do negócio)
                 │
                 └── 1:N ── ItemDetalhe (Atributos e sub-itens)
```

---

## 2. Conceitos e Entidades Principais

### 2.1 Usuário (`Usuario`)
Representa qualquer agente humano que interage com o sistema autenticado.

- **Responsabilidade**: Manter a identidade, credenciais e permissões de acesso ao sistema.
- **Principais Informações**:
  - `id`: Identificador único no backend Xano.
  - `nome`: Nome completo do usuário.
  - `email`: Endereço de e-mail (usado para login e contato).
  - `role`: Perfil de acesso (ex.: Aluno, Professor, Administrador).
  - `criado_em`: Data e hora de criação da conta.
- **Relacionamentos**:
  - Um usuário pode gerenciar múltiplos recursos e gerar múltiplos registros de atividade.
- **Regras Estruturais**:
  - O e-mail deve ser único no sistema.
  - Senhas são tratadas e criptografadas exclusivamente no Xano.

---

### 2.2 Recurso Principal (`Recurso`)
Representa o objeto central de valor da aplicação (ex.: Projeto, Tarefa, Pedido, Produto, Conforme o tema do grupo).

- **Responsabilidade**: Encapsular o ciclo de vida e estado do dado principal manipulado pelos usuários.
- **Principais Informações**:
  - `id`: Identificador único.
  - `titulo`: Nome ou identificação descritiva do recurso.
  - `descricao`: Detalhamento textual.
  - `status`: Estado atual (ex.: Pendente, Em Progresso, Concluído, Cancelado).
  - `criado_por`: Associação com o `Usuario` criador.
  - `atualizado_em`: Data e hora da última modificação.
- **Relacionamentos**:
  - Pertence a um `Usuario`.
  - Pode possuir uma lista de `ItemDetalhe`.
- **Regras Estruturais**:
  - Um recurso não pode ser criado sem um criador autenticado válido.
  - Apenas o criador ou administradores podem atualizar ou excluir o recurso.

---

### 2.3 Registro de Atividade / Auditoria (`RegistroAtividade`)
Registra eventos relevantes ocorridos no sistema.

- **Responsabilidade**: Rastreabilidade e histórico de operações críticas.
- **Principais Informações**:
  - `id`: Identificador único.
  - `acao`: Descrição do evento (ex.: `CRIACAO_RECURSO`, `LOGIN`, `ALTERACAO_STATUS`).
  - `data_hora`: Carimbo de tempo do evento.
  - `usuario_id`: Usuário associado à ação.
- **Relacionamentos**:
  - Pertence a um `Usuario`.
- **Regras Estruturais**:
  - Registros de auditoria são imutáveis (apenas inserção e leitura, sem exclusão física).

---

## 3. Diretrizes de Evolução do Modelo
- Este modelo conceitual fornece a visão global inicial.
- A persistência física (tabelas e campos específicos no Xano) será implementada de maneira incremental por meio das Changes do OpenSpec.
- Novas entidades ou atributos devem ser propostos e revisados dentro do fluxo `explore → propose` do OpenSpec antes de serem criados no banco.
