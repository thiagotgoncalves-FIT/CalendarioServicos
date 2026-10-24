## 1. Backup e Inventário de Dados

- [x] 1.1 Exportar backup completo de todas as 6 tabelas para a pasta `backups/backup_2026-10-18_pre_cleanup/` (JSON e .xs) e garantir exclusão no `.gitignore`
- [x] 1.2 Mapear chaves estrangeiras e inventariar contagens atuais por tabela

## 2. Dry-Run e Confirmação com o Usuário

- [x] 2.1 Preparar tabela de dry-run (antes vs depois) e apresentar ao usuário para confirmação explícita
- [x] 2.2 Coletar decisão do usuário sobre a grafia do nome de exibição do Hector ("Hector Barros" vs "Hector Bernardes")

## 3. Execução da Limpeza no Xano

- [x] 3.1 Ajustar os registros locais nas tabelas dependentes (`cliente.xs` e `event_log.xs`), zerando itens de usuários antigos
- [x] 3.2 Ajustar os registros locais em `user.xs`, mantendo estritamente o registro de Hector (id 15, role prestador)
- [x] 3.3 Executar validação de prévia e integridade no Xano
- [x] 3.4 Executar limpeza no Xano mantendo unicamente Hector Barros (id 15)

## 4. Verificação Pós-Limpeza

- [x] 4.1 Confirmar contagem final por tabela no Xano e integridade da estrutura (campos e índices intactos)
- [x] 4.2 Testar login do Hector com credenciais reais e verificar geração de token JWT
- [x] 4.3 Testar signup de um usuário de teste cliente com senha em hash no Xano, registrar evidência e apagar o usuário de teste
