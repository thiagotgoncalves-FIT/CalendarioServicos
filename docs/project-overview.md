# Project Overview — Projeto Integrador (Innovation Lab)

## 1. Visão Geral
Este repositório abriga o projeto integrador da disciplina **Innovation Lab: Advanced No/Low Code** (Faculdade IMPACTA). O objetivo do projeto é desenvolver uma aplicação completa orientada pelo paradigma **Spec-Driven Development (SDD)**, com apoio do agente de Inteligência Artificial no ambiente **Antigravity**.

## 2. Problema
O desenvolvimento de produtos digitais frequentemente sofre com desalinhamento entre requisitos e código, complexidade de manutenção de backends tradicionais e amnésia de contexto em ferramentas de IA. Este projeto resolve esse problema através da combinação de um backend gerenciado (Xano), um frontend ágil em Python (Streamlit) e uma fundação documental sólida via OpenSpec.

## 3. Objetivos
- Estabelecer uma aplicação robusta de ponta a ponta (Frontend, Backend, Integrações e Banco de Dados).
- Conectar uma interface web moderna a endpoints de API REST no Xano.
- Praticar desenvolvimento guiado por especificações estruturadas antes da implementação do código.
- Garantir histórico versionado e rastreabilidade pelo Git/GitHub.

## 4. Público-Alvo e Personas
- **Usuários Finais**: Acessam a aplicação para realizar operações do domínio do sistema (consultar dados, submeter formulários, autenticar e acompanhar status).
- **Administradores**: Gerenciam registros, configurações e permissões.
- **Desenvolvedores / Alunos**: Evoluem as funcionalidades de forma iterativa via OpenSpec.

## 5. Escopo Inicial (MVP)
- **Fase 1 (Ambiente & Contexto)**: Estrutura base do projeto configurada (OpenSpec, Streamlit, Xano CLI e MCP, Git).
- **Fase 2 (Backend Base no Xano)**: Modelagem de entidades essenciais, autenticação e primeiros endpoints REST.
- **Fase 3 (Frontend Base no Streamlit)**: Telas de login/registro, listagem e formulários de cadastro.
- **Fase 4 (Integração & Refinamento)**: Consumo das APIs do Xano no Streamlit, tratamento de erros e validações.

## 6. Principais Funcionalidades
- Autenticação e autorização de usuários.
- Operações de leitura e escrita (CRUD) refletidas em tempo real no banco Xano.
- Painéis informativos e formulários responsivos no Streamlit.
- Tratamento resiliente de respostas de API e mensagens amigáveis de feedback.

## 7. Requisitos e Restrições Importantes
- **Frontend**: Streamlit será utilizado como tecnologia exclusiva para implementação do frontend da aplicação.
- **Backend**: Xano será a tecnologia de backend para regras de negócio, tabelas de banco de dados e APIs REST.
- **Ambiente de IA**: Antigravity IDE utilizado em conjunto com o OpenSpec.
- **Xano Developer MCP**: Utilizado pelo agente de IA para documentação e validação de XanoScript (`.xs`).

## 8. Arquitetura Tecnológica
- **Frontend**: Streamlit (Python 3.14)
- **Backend & Banco de Dados**: Xano (No-Code / Low-Code & XanoScript)
- **Integração**: Requisições HTTP / REST (JSON)
- **Desenvolvimento Assistido por IA**: OpenSpec (Spec-Driven Development)
- **Controle de Versão**: Git & GitHub

## 9. Princípios de Desenvolvimento
- Especificação antes da implementação (nenhum código sem spec correspondente).
- Implementação incremental em fatias funcionais verticais.
- Evitar retrabalho e manter a documentação viva sincronizada com o código.
- Simplicidade e clareza no design e na lógica.

## 10. Segurança e Integridade
- Regras de autorização e integridade de dados devem ser aplicadas no backend (Xano).
- O frontend não deve ser considerado mecanismo de segurança exclusivo.
- Credenciais e tokens sensíveis não devem ser comitados no repositório (`.env` protegido pelo `.gitignore`).

## 11. Estratégia de Desenvolvimento
O desenvolvimento segue o ciclo em cinco etapas do OpenSpec:
1. `Explore`: Análise e investigação antes da criação da mudança.
2. `Propose`: Criação dos artefatos de especificação (`proposal.md`, `specs/`, `design.md`, `tasks.md`).
3. `Review`: Validação humana dos requisitos e do design técnico.
4. `Apply`: Implementação rigorosa do checklist definido em `tasks.md`.
5. `Archive`: Consolidação da mudança na especificação permanente e histórico.

## 12. Fonte de Verdade e Documentação
- `docs/project-overview.md`: Apresentação global estável do projeto.
- `docs/domain-model.md`: Modelo conceitual de domínio.
- `AGENTS.md`: Diretrizes e regras operacionais para o agente Antigravity.
- `openspec/specs/`: Requisitos consolidados do sistema.
- `openspec/changes/`: Propostas de mudanças em andamento.
