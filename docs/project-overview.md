# Project Overview — AgendAí (Gestão e Agendamento para Prestadores Independentes)

## 1. Visão Geral
O **AgendAí** é uma plataforma web desenvolvida para simplificar e automatizar o processo de agendamento de horários e gestão de serviços para pequenos prestadores autônomos e independentes (barbeiros, personal trainers, manicures, tutores, psicólogos, massoterapeutas, entre outros) e seus clientes.

O projeto é concebido e desenvolvido no âmbito da disciplina **Innovation Lab: Advanced No/Low Code** (Faculdade IMPACTA - Prof. Leonardo Bontempo), utilizando o paradigma **Spec-Driven Development (SDD)** suportado pelo **OpenSpec**, com backend serverless no **Xano** e interface web ágil em **Streamlit**.

## 2. O Problema
Profissionais autônomos e microempreendedores individuais gastam em média de 1 a 3 horas diárias trocando mensagens manuais no WhatsApp para conciliar horários com clientes. Esse modelo descentralizado acarreta:
- **Conflitos de agenda (Double Booking)**: Marcações duplicadas para o mesmo intervalo de tempo.
- **Falta de comparecimento e furos (No-shows)**: Clientes esquecem horários agendados sem lembretes centralizados.
- **Perda de clientes e faturamento**: Dificuldade em responder prontamente a solicitações em horários de atendimento ou fora do expediente comercial.
- **Falta de visibilidade financeira e operacional**: Dificuldade em apurar o histórico de atendimentos e a previsão de receita semanal/mensal.

## 3. A Solução
O **AgendAí** oferece um fluxo simplificado e intuitivo de ponta a ponta:
1. **Para o Prestador**:
   - Cadastro e gestão do perfil profissional.
   - Configuração de catálogo de serviços (título, descrição, duração e preço).
   - Definição de horários de atendimento e dias de funcionamento.
   - Painel de controle (Dashboard) com visualização dos agendamentos do dia, semana e status (Pendente, Confirmado, Concluído, Cancelado).
2. **Para o Cliente**:
   - Acesso simplificado ao catálogo de serviços do profissional.
   - Seleção do serviço desejado e visualização em tempo real dos horários livres (evitando conflitos).
   - Agendamento ágil em poucos cliques, com confirmação e histórico de agendamentos.

## 4. Por que é Ideal para o Ciclo de 6 Meses
- **Escopo Bem Definido e Focado**: Problema claro com limites bem delimitados, permitindo entrega de valor rápida e iterativa.
- **Alto Valor Prático para Avaliação**: Resolve uma dor real de mercado com impacto imediato, facilitando a demonstração para bancas e professores.
- **Cobertura de Regras de Negócio Críticas de Desenvolvimento Web**:
  - Autenticação e Autorização (perfis distintos: Prestador vs. Cliente).
  - CRUD Completo (Serviços, Horários de Trabalho e Agendamentos).
  - Manipulação e Validação de Datas/Horários (cálculo de slots livres com base na duração do serviço, bloqueio de sobreposições e impedimento de marcações no passado).
  - Transições de Estado de Negócio (Pendente ➔ Confirmado ➔ Concluído / Cancelado).

## 5. Público-Alvo e Personas
- **Prestador de Serviço Independente (Persona Principal)**: Profissional autônomo que necessita gerenciar seu catálogo de serviços, sua agenda semanal e otimizar seu tempo de trabalho.
- **Cliente Final**: Pessoa física que contrata os serviços do prestador e busca comodidade, transparência de preços e rapidez para reservar um horário.
- **Administrador da Plataforma (Opcional/Futuro)**: Responsável por métricas globais, auditoria e suporte do sistema.

## 6. Escopo do MVP (Milestones de 6 Meses)
- **Fase 1 (Fundação & Setup)**: Estrutura base de SDD (OpenSpec), repositório Git, ambiente Streamlit e integração Xano CLI/MCP.
- **Fase 2 (Autenticação & Perfis no Xano/Streamlit)**: Cadastro, login e segregação de permissões (Prestador vs. Cliente) com persistência no Xano.
- **Fase 3 (Catálogo de Serviços & Disponibilidade)**: CRUD de serviços (nome, duração, valor) e configuração da grade de horários de trabalho do prestador.
- **Fase 4 (Motor de Agendamento)**: Lógica no Xano para cálculo de horários livres, prevenção de conflitos de horário e criação do agendamento pelo cliente.
- **Fase 5 (Gestão da Agenda & Status)**: Painel do prestador para aprovar, confirmar, concluir ou cancelar agendamentos, e tela de acompanhamento para o cliente.
- **Fase 6 (Refinamento & Apresentação)**: Filtros, relatórios/métricas simples (total faturado, agendamentos realizados), validações de erro amigáveis e documentação final consolidada.

## 7. Principais Funcionalidades do Sistema
- **Módulo de Autenticação**: Cadastro/login com JWT seguro gerenciado pelo Xano.
- **Módulo de Serviços**: Cadastro de serviços com título, descrição, duração (ex: 30min, 60min) e preço.
- **Módulo de Horários**: Definição de dias da semana atendidos e intervalos de expediente.
- **Módulo de Reserva**: Interface de seleção de data, visualização de horários disponíveis e submissão da reserva.
- **Módulo de Gestão (Dashboard)**: Visualização da agenda diária/semanal e alteração dos status do agendamento.
- **Módulo de Notificação/Feedback**: Mensagens contextuais e claras sobre o status das operações.

## 8. Arquitetura Tecnológica
- **Frontend**: [Streamlit](https://streamlit.io/) (Python 3.14) — Tecnologia exclusiva para as interfaces web da aplicação.
- **Backend & Banco de Dados**: [Xano](https://www.xano.com/) — Modelagem relacional, APIs REST, autenticação nativa e regras de negócio com XanoScript.
- **Comunicação**: REST API via chamadas HTTP (JSON).
- **Metodologia de Engenharia**: [OpenSpec](https://openspec.dev/) — Spec-Driven Development (SDD) com governança por IA.
- **Ambiente de Desenvolvimento**: Google Antigravity IDE com Xano Developer MCP.
- **Controle de Versão**: Git e GitHub.

## 9. Princípios de Desenvolvimento
- **Spec-Driven**: Nenhuma funcionalidade é codificada sem uma especificação prévia (`proposal.md`, `specs/`, `design.md`, `tasks.md`).
- **Validação no Backend**: O cálculo de horários válidos e a integridade de dados devem ser garantidos no Xano (evitando concorrência ou reservas duplicadas).
- **Simplicidade e Usabilidade**: Telas limpas, intuitivas e focadas na facilidade de uso para usuários não técnicos.

## 10. Segurança e Integridade
- Senhas criptografadas exclusivamente pelo Xano (bcrypt).
- Autenticação baseada em tokens com expiração e verificação de perfil de acesso (`role`).
- Isolamento de dados: Um prestador só acessa e altera seus próprios serviços e agendamentos.
- Variáveis sensíveis e URLs de API mantidas em `.env` (ignorado no Git).

## 11. Fonte de Verdade e Documentação
- `docs/project-overview.md`: Este documento (visão e escopo global).
- `docs/domain-model.md`: Modelo conceitual de entidades e regras de negócio.
- `AGENTS.md`: Regras de conduta para o agente no Antigravity.
- `openspec/config.yaml`: Diretrizes metodológicas do projeto.
- `openspec/specs/`: Especificações consolidadas de funcionalidades.
- `openspec/changes/`: Ciclos de propostas de novas fatias verticais.

---

## 12. Processo de Desenvolvimento Obrigatório (OpenSpec SDD)

Toda nova funcionalidade **obrigatoriamente** deve percorrer este ciclo antes de qualquer implementação:

| Etapa | Comando | O que acontece | Pode escrever código? |
|---|---|---|---|
| 1. Explore | `/opsx-explore` | Investigar, mapear dependências, entender o problema | NÃO |
| 2. Propose | `/opsx-propose` | Gerar `proposal.md`, `specs/`, `design.md`, `tasks.md` | NÃO |
| 3. Review | *(manual)* | Grupo valida e aprova todos os artefatos | NÃO |
| 4. Apply | `/opsx-apply` | Implementar seguindo `tasks.md` como checklist | SIM |
| 5. Archive | `/opsx-archive` | Consolidar specs e arquivar a change concluída | NÃO |

> **Regra de ouro**: A IA propõe — o grupo analisa — o grupo aprova — a IA implementa. A saída da IA não é automaticamente correta.

### Princípios inegóciáveis
- **Entrega vertical**: cada Change entrega uma fatia completa (Xano backend + Streamlit frontend + spec).
- **Incremental**: uma funcionalidade por vez. Nunca implementar tudo de uma só vez.
- **DB acompanha a feature**: tabelas são criadas no Xano na medida em que as funcionalidades são desenvolvidas — não antecipadamente.
- **Escopo pequeno e verificável**: cada Change deve poder ser verificada de forma independente.

---

## 13. Roadmap de Changes (Fatias Verticais)

O projeto é entregue em Changes sequenciais, cada uma com escopo vertical próprio:

| Change | Nome | Status | Capabilities |
|---|---|---|---|
| C1 | `autenticacao-e-perfis` | ✅ Arquivada | Cadastro, login JWT, sessão, logout, roles |
| C2 | `catalogo-e-disponibilidade` | ✅ Arquivada | CRUD de serviços, grade semanal de horários |
| C3 | `motor-de-agendamento` | ⏳ Planejada (Próxima) | Cálculo de slots livres, criação de reserva, anti-double-booking |
| C4 | `gestao-agenda-e-status` | ⏳ Planejada | Painel do prestador, ciclo de status, histórico do cliente |
| C5 | `refinamento-e-metricas` | ⏳ Planejada | Dashboard financeiro, filtros, UX final, documentacao |

> **Toda nova funcionalidade não prevista neste roadmap deve iniciar obrigatoriamente pelo `/opsx-explore` antes de qualquer proposta.**
