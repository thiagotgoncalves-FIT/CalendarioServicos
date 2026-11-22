## 1. Persistência e Reconciliação do Avatar

- [x] 1.1 Implementar a função auxiliar `_enrich_user_avatar` em `services/auth_service.py` que inspeciona o diretório `uploads/avatars/` procurando arquivos existentes vinculados ao `user_id` e preenche `photo_url` e `photo_rel_url`.
- [x] 1.2 Integrar a reconciliação automática de avatar nos métodos de autenticação e consulta de usuário (`login`, `get_current_user`, `signup` e `update_user_profile`) em `services/auth_service.py`.
- [x] 1.3 Assegurar na função `save_user_avatar` que qualquer imagem anterior com outra extensão seja removida antes de gravar o novo arquivo, mantendo o diretório consistente.

## 2. Redesign e Reposicionamento do Usuário na Barra Lateral

- [x] 2.1 Reestruturar o topo da barra lateral em `app.py`, unificando a marca "AgendAí" com a identificação do usuário logado (avatar, nome, e-mail e badge) em posição superior imediata, eliminando lacunas de espaçamento.
- [x] 2.2 Ajustar os botões de ação do sidebar ("⚙️ Configurações" e "Sair") para alinhamento harmonioso logo abaixo do cartão superior do perfil.
- [x] 2.3 Ajustar regras de CSS em `services/ui_utils.py` para não ocultar o botão de toggle/reabertura da barra lateral (`stSidebarCollapsedControl`).
- [x] 2.4 Implementar estilização de mini barra lateral retrátil (mantendo largura de ícones acessível ao recolher).

## 3. Testes e Validação

- [x] 3.1 Atualizar `test_user_settings.py` para incluir teste de re-login com avatar pré-existente no disco e verificar que a imagem é preservada e retornada.
- [x] 3.2 Executar a suíte de testes completa do projeto e validar a change com `openspec validate redesign-layout-e-persistencia-avatar --strict`.
