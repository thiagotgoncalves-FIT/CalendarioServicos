# AgendAí — Plataforma de Gestão e Agendamento para Prestadores Independentes

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Xano](https://img.shields.io/badge/backend-Xano-red.svg)](https://www.xano.com/)
[![OpenSpec](https://img.shields.io/badge/spec--driven-OpenSpec-green.svg)](https://openspec.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Projeto desenvolvido para a disciplina **Innovation Lab: Advanced No/Low Code** (Faculdade IMPACTA - Prof. Leonardo Bontempo).

---

## 💡 Sobre o Projeto

O **AgendAí** é uma aplicação web desenvolvida para eliminar o atrito de agendamentos manuais via WhatsApp entre pequenos profissionais autônomos (barbeiros, personal trainers, manicures, tutores, psicólogos) e seus clientes.

### O Problema
Profissionais independentes gastam horas diárias trocando mensagens para conciliar horários, enfrentando:
- **Conflitos de agenda (*Double Booking*)**: marcações sobrepostas para o mesmo horário.
- **Falta de comparecimento (*No-shows*)**: ausência de confirmação e histórico centralizado.
- **Desorganização de catálogo e preços**: clientes sem clareza dos serviços oferecidos e valores.

### A Solução
- **Para o Prestador**: cadastro de serviços com precificação e duração em minutos, definição de grade semanal de expediente com intervalo de almoço, painel administrativo com alteração de status (Confirmar, Concluir, Cancelar), exportação de relatórios em CSV e botões de contato direto/lembrete via WhatsApp para eliminar *no-shows*.
- **Para o Cliente**: acesso ao catálogo de serviços, seleção de datas com cálculo em tempo real de horários livres disponíveis (slots de 30 min), confirmação imediata da reserva e acompanhamento no painel "Meus Agendamentos".

---

## 🛠️ Tecnologias Utilizadas

- **Frontend**: [Streamlit](https://streamlit.io/) — Interface responsiva em Dark Theme profissional com glassmorphism.
- **Backend & Banco de Dados**: [Xano](https://www.xano.com/) — Modelagem relacional, regras serverless, autenticação JWE/JWT nativa com hash seguro de senhas via XanoScript (`.xs`).
- **Sincronização CLI**: [Xano CLI (`@xano/cli`)](https://docs.xano.com/xano-cli/get-started) — Gerenciamento e deploy dos endpoints locais diretamente para a nuvem.
- **Metodologia de Engenharia**: [OpenSpec](https://openspec.dev/) — Spec-Driven Development (SDD) com governança estrita de ciclo de vida (`Explore` → `Propose` → `Review` → `Apply` → `Archive`).
- **Linguagem & Ambiente**: Python 3.10+, Requests, python-dotenv.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir instalado em sua máquina:
- **Python** (versão 3.10 a 3.14)
- **Git**
- **Node.js** (versão 18 ou superior — necessário para o Xano CLI)
- **Xano CLI**:
  ```bash
  npm install -g @xano/cli
  ```

---

## ⚙️ Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/thiagotgoncalves-FIT/CalendarioServicos.git
cd CalendarioServicos
```

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente
Copie o modelo `.env.example` para `.env`:
```bash
cp .env.example .env
```
Edite o arquivo `.env` com as configurações da sua instância do Xano:
```dotenv
XANO_API_URL=https://x8ki-letl-twmt.n7.xano.io/api:M19UcCw4
USE_MOCK_FALLBACK=False
```
> **Nota de Segurança:** O arquivo `.env` contém chaves e URLs reais e é ignorado pelo Git via `.gitignore`. Nunca realize commits de arquivos de ambiente com credenciais.

---

## 🚀 Como Executar o Projeto

Com o ambiente virtual ativado:
```bash
streamlit run app.py
```
Abra o navegador no endereço: `http://localhost:8501`

---

## 🧪 Como Rodar os Testes

O projeto conta com baterias de testes integrados e funcionais que validam tanto a conexão ao vivo com o Xano quanto a robustez das regras de negócio do motor de agendamentos:

### 1. Teste de Autenticação, Perfis e Isolamento:
Valida cadastro real com hash, login com senha válida/inválida, bloqueio de e-mails duplicados e consulta de perfil `/auth/me`:
```bash
python test_roles_isolation.py
```

### 2. Teste do Motor de Agendamento:
Valida cálculo de slots de 30 min, bloqueio de horários passados, respeito a expediente/almoço, prevenção contra *double-booking* e transições de status:
```bash
python test_appointment_engine.py
```

### 3. Validação de Especificações OpenSpec:
```bash
openspec validate --all
```

---

## 📁 Estrutura de Pastas

```text
Projeto/
├── .agents/                    # Workflows e skills do OpenSpec
├── .gemini/                    # Configurações do Antigravity
├── .streamlit/                 # Configurações de tema nativo (Dark Theme)
│   └── config.toml
├── docs/                       # Documentação de arquitetura e modelo de domínio
│   ├── project-overview.md     # Visão geral e roadmap do projeto
│   └── domain-model.md         # Modelo conceitual de entidades e regras
├── openspec/                   # Especificações Spec-Driven Development
│   ├── config.yaml             # Configuração e regras dos fluxos do OpenSpec
│   ├── specs/                  # Documentação viva e consolidada das capacidades
│   │   ├── appointment-engine/ # Especificação do motor de agendamentos
│   │   ├── prestador-availability/
│   │   ├── service-catalog/
│   │   └── user-auth/          # Especificação de autenticação e perfis
│   └── changes/
│       └── archive/            # Histórico rastreável de changes concluídas
├── services/                   # Camada de serviços e clientes de API
│   ├── api_client.py           # Cliente HTTP centralizado com headers JWT
│   ├── appointment_service.py  # Motor de cálculo de slots e reservas
│   ├── auth_service.py         # Autenticação, hash, signup e login
│   ├── availability_service.py # Grade de horários e expediente
│   └── catalog_service.py      # Gestão do catálogo de serviços
├── xano/                       # Arquivos locais sincronizados com XanoScript (.xs)
├── .env.example                # Modelo de variáveis de ambiente sem segredos
├── .gitignore                  # Arquivos e pastas excluídos do Git
├── AGENTS.md                   # Diretrizes operacionais para desenvolvimento com IA
├── app.py                      # Aplicação web completa em Streamlit
├── requirements.txt            # Dependências Python
├── test_appointment_engine.py # Testes de agendamento e anti-double-booking
├── test_roles_isolation.py     # Testes de autenticação e segregação de dados
└── README.md                   # Este manual
```

---

## 💡 Exemplos de Uso

1. **Cadastro de Usuário**:
   - Acesse a aba "Cadastrar", selecione o perfil (**Prestador** ou **Cliente**) e informe nome, e-mail, telefone e senha (mínimo de 8 caracteres, com letra e número).
   - O registro é gravado com hash criptográfico seguro no Xano e o token JWT é emitido imediatamente.
2. **Gerenciamento do Catálogo (Prestador)**:
   - Crie novos serviços informando título, descrição, duração (ex.: 30 ou 60 minutos) e preço em Reais.
3. **Agendamento em Tempo Real (Cliente)**:
   - Na visão do cliente, selecione a data desejada. O sistema calcula automaticamente os slots vagos descartando horários já preenchidos e intervalos de almoço.
   - Ao confirmar, o horário é reservado atomicamente, impedindo colisões com outros clientes.

---

## 🤝 Como Contribuir

1. Crie uma branch para a sua funcionalidade:
   ```bash
   git checkout -b feature/minha-feature
   ```
2. Siga obrigatoriamente a metodologia **OpenSpec**:
   - Nunca altere código sem uma especificação aberta (`openspec new change`).
   - Siga o checklist de tarefas em `tasks.md`.
3. Valide suas alterações com os testes automatizados e o `openspec validate --all`.
4. Abra um Pull Request detalhando as mudanças realizadas.

---

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos na **Faculdade IMPACTA** e está sob a licença [MIT](LICENSE).
