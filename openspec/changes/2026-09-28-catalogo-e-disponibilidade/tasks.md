## 1. Camada de Serviços e Integração Frontend

- [ ] 1.1 Criar módulo `services/catalog_service.py` com suporte a chamadas REST ao Xano (`GET`, `POST`, `PUT`) e dados simulados para desenvolvimento local.
- [ ] 1.2 Criar módulo `services/availability_service.py` com suporte à leitura e gravação da grade semanal de horários e validações de consistência cronológica.

## 2. Interface do Catálogo de Serviços no Streamlit

- [ ] 2.1 Implementar aba "✂️ Meus Serviços" no Painel do Prestador com formulário de novo serviço (título, descrição, preço em BRL e duração em minutos).
- [ ] 2.2 Exibir listagem de serviços cadastrados com cards visuais, badges de status ativo/inativo e opção de desativação/reativação.
- [ ] 2.3 Atualizar métricas do prestador (quantidade de serviços ativos e preço médio) no dashboard.

## 3. Interface da Grade de Disponibilidade no Streamlit

- [ ] 3.1 Implementar aba "🕒 Grade de Atendimento" permitindo ativar/desativar dias da semana e definir horário de início, término e intervalo.
- [ ] 3.2 Implementar validações visuais em tempo real para impedir horários de término inferiores ao início ou pausas fora do expediente.
- [ ] 3.3 Adicionar botão de salvamento com feedback de confirmação.

## 4. Integração na Área do Cliente e Validação

- [ ] 4.1 Implementar exibição do catálogo de serviços disponíveis na Área do Cliente para permitir visualização pública das ofertas.
- [ ] 4.2 Testar a alternância entre prestador e cliente verificando consistência e isolamento dos dados.
