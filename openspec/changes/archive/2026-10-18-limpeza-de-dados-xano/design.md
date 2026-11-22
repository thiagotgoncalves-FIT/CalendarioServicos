# Design Técnico: Limpeza de Dados e Isolamento Relacional no Xano

## Context
Ver `proposal.md` para motivação e justificativa. O banco de dados no Xano possui 6 tabelas (`account`, `agent_conversation`, `agent_message`, `cliente`, `event_log`, `user`). A tabela `user` contém 14 registros, dos quais 13 são usuários de teste antigos ou inválidos e 1 é o prestador Hector (id 15). A tabela `cliente` possui 1 registro e `event_log` possui 10 registros vinculados a usuários antigos.

## Goals / Non-Goals

**Goals:**
- Garantir backup completo em disco local fora do git antes de qualquer alteração destrutiva.
- Eliminar dependências relacionais na ordem estrita de chaves estrangeiras: primeiro `cliente` e `event_log` (tabelas dependentes), e depois a tabela `user`.
- Manter exclusivamente o registro do Hector Barros (id 15, role `prestador`, account_id 0, senha em hash intacta).
- Validar via `--dry-run` antes de aplicar a sincronização para o workspace remoto no Xano.
- Confirmar integridade estrutural das tabelas e índices.

**Non-Goals:**
- Não alterar schema (sem renomear colunas, tipos ou índices).
- Não remover tabelas, endpoints ou grupos de API.
- Não redefinir senhas ou tokens existentes do Hector.

## Decisions

### 1. Ordem de Exclusão Relacional
- **Decisão**: Limpar tabelas dependentes antes de limpar `user`.
  - 1º: `cliente` (remover registro id 1 que referencia user_id 4)
  - 2º: `event_log` (remover 10 registros que referenciam user_id 2, 3, 4)
  - 3º: `user` (remover ids 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14; reter apenas id 15)
- **Alternativa descartada**: Apagar diretamente em `user`, o que causaria violação de integridade referencial ou registros órfãos.

### 2. Estratégia de Backup
- **Decisão**: Backup duplo em `backups/backup_2026-10-18_pre_cleanup/` contendo arquivos `.xs` originais completos e arquivos `.json` estruturados para cada uma das 6 tabelas.
- **Alternativa descartada**: Apenas backup manual em memória, que não protege contra falhas.

### 3. Sincronização via Xano CLI com Dry-Run Obrigatório
- **Decisão**: Utilizar `xano workspace push -w 147997 -d ./xano --records --dry-run` para pré-visualização e confirmação antes de qualquer push definitivo com `--records`.
- **Alternativa descartada**: Chamadas ad-hoc sem controle de versão ou sem dry-run.

## Risks / Trade-offs

- **[Risco de perda acidental de dados]** → Mitigado pelo backup JSON e .xs em `backups/` (ignorado no git) antes de iniciar a limpeza.
- **[Risco de quebra de login do Hector]** → Mitigado mantendo o hash de senha exato e campos estruturais inalterados.
- **[Risco de alteração estrutural involuntária]** → Mitigado por restringir a alteração unicamente ao bloco `items = [...]` dos arquivos `.xs` de tabelas.
