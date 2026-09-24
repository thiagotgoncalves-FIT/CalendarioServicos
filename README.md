# Projeto Integrador — Innovation Lab: Advanced No/Low Code

Projeto desenvolvido para a disciplina **Innovation Lab: Advanced No/Low Code** (Faculdade IMPACTA - Prof. Leonardo Bontempo).

---

## 🛠️ Tecnologias Utilizadas

- **Frontend**: [Streamlit](https://streamlit.io/) (Python 3.14)
- **Backend & Database**: [Xano](https://www.xano.com/) (No-Code / Low-Code & XanoScript)
- **Engenharia de IA & Metodologia**: [OpenSpec](https://openspec.dev/) (Spec-Driven Development)
- **IDE & Ferramenta de IA**: Google Antigravity
- **MCP Server**: Xano Developer MCP (`@xano/developer-mcp`)
- **Versionamento**: Git & GitHub

---

## 📁 Estrutura do Projeto

```text
Projeto/
├── .agents/                    # Workflows e skills do OpenSpec + MCP config para Antigravity
│   ├── mcp_config.json
│   ├── skills/
│   └── workflows/
├── .gemini/                    # Configurações do Antigravity / Gemini
│   └── settings.json
├── .venv/                      # Ambiente virtual Python (ignorado no Git)
├── docs/                       # Fundação documental de contexto
│   ├── project-overview.md     # Visão geral, arquitetura e requisitos
│   └── domain-model.md         # Modelo conceitual de domínio
├── openspec/                   # Estrutura do Spec-Driven Development
│   ├── config.yaml             # Configuração global, contexto e regras do OpenSpec
│   ├── specs/                  # Especificações consolidadas permanentes
│   └── changes/                # Mudanças em andamento e histórico
│       └── archive/
├── xano/                       # Arquivos locais sincronizados do Xano (.xs)
├── .gitignore                  # Regras de exclusão do Git
├── AGENTS.md                   # Diretrizes operacionais para o agente Antigravity
├── app.py                      # Aplicação frontend Streamlit
├── requirements.txt            # Dependências Python congeladas
└── README.md                   # Este manual
```

---

## 🚀 Como Executar o Projeto

### 1. Ativar o Ambiente Virtual Python

No terminal do Antigravity (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

Caso utilize Prompt de Comando (CMD):
```cmd
.venv\Scripts\activate.bat
```

### 2. Executar o Frontend Streamlit

Com o `.venv` ativado:
```bash
streamlit run app.py
```
Acesse no seu navegador: `http://localhost:8501`

---

## ⚙️ Operações com o Xano CLI

O Xano CLI já está instalado globalmente (`@xano/cli`). Para conectar sua conta e gerenciar seus arquivos locais:

1. **Autenticar**:
   ```bash
   xano auth
   ```
2. **Verificar conexão**:
   ```bash
   xano profile me
   ```
3. **Baixar o código do workspace para a pasta local `xano/`**:
   ```bash
   xano workspace pull -d ./xano
   ```
4. **Verificar diferenças antes de enviar**:
   ```bash
   xano workspace push -d ./xano --dry-run
   ```
5. **Enviar atualizações para o Xano**:
   ```bash
   xano workspace push -d ./xano
   ```

---

## 🤖 Como Operar o OpenSpec no Antigravity

O OpenSpec já está configurado com as ferramentas e comandos nativos para o Antigravity:

1. **Mapeamento e Investigação**:
   Peça ao agente ou use `/opsx-explore` para analisar o projeto e propor fatias incrementais de valor.
2. **Propor uma Funcionalidade**:
   ```text
   /opsx-propose "Nome da funcionalidade"
   ```
3. **Revisar a Especificação**:
   Valide os artefatos gerados (`proposal.md`, `specs/`, `design.md`, `tasks.md`).
4. **Implementar**:
   ```text
   /opsx-apply
   ```
5. **Arquivar e Consolidar**:
   ```text
   /opsx-archive
   ```

---

## 🌿 Comandos Essenciais do Git

```bash
git status                     # Verificar o estado do repositório
git add .                      # Adicionar modificações ao staging
git commit -m "feat: ..."      # Gravar commit com mensagem semântica
```
