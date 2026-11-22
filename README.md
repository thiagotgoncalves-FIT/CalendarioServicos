# CalendarioServico — Manual de Uso do Aplicativo Web

[![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Xano](https://img.shields.io/badge/backend-Xano-red.svg)](https://www.xano.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![OpenSpec](https://img.shields.io/badge/spec--driven-OpenSpec-green.svg)](https://openspec.dev/)

Projeto desenvolvido para a disciplina **Innovation Lab: Advanced No/Low Code** — Faculdade IMPACTA (Prof. Leonardo Bontempo).

**Integrantes:** Bruno Teixeira · Thiago Tavares · Hector Barros · Andre Greggersen

**Repositório:** <https://github.com/thiagotgoncalves-FIT/CalendarioServicos>

---

## Sumário

1. [Apresentação](#1-apresentação)
2. [Acesso ao aplicativo](#2-acesso-ao-aplicativo)
3. [Perfis de usuários](#3-perfis-de-usuários)
4. [Funcionalidades](#4-funcionalidades)
5. [Manual de utilização](#5-manual-de-utilização)
   - [5.1 Primeiros passos (todos os perfis)](#51-primeiros-passos-todos-os-perfis)
   - [5.2 Jornada do Prestador](#52-jornada-do-prestador)
   - [5.3 Jornada do Cliente](#53-jornada-do-cliente)
   - [5.4 Configurações da conta (todos os perfis)](#54-configurações-da-conta-todos-os-perfis)
6. [Exemplos de utilização](#6-exemplos-de-utilização)
7. [Limitações conhecidas](#7-limitações-conhecidas)
8. [Ciclo de vida de um agendamento](#8-ciclo-de-vida-de-um-agendamento)
9. [Mensagens comuns e solução de problemas](#9-mensagens-comuns-e-solução-de-problemas)
10. [Informações técnicas](#10-informações-técnicas)

---

## 1. Apresentação

### O que é

O **CalendarioServico** (exibido na interface como **AgendAí**) é um aplicativo web de agendamento online que conecta **prestadores de serviço autônomos** — barbeiros, manicures, personal trainers, tutores, psicólogos, massoterapeutas, entre outros — aos seus **clientes**.

O prestador publica seus serviços, preços e horários de trabalho; o cliente escolhe o serviço, vê apenas os horários realmente livres e reserva em poucos cliques.

### Problema que resolve

Profissionais autônomos costumam combinar horários manualmente pelo WhatsApp, o que gera:

- **Conflitos de agenda (*double booking*)** — dois clientes marcados no mesmo horário;
- **Faltas (*no-shows*)** — clientes esquecem o horário por falta de confirmação e lembrete;
- **Falta de clareza** — o cliente não sabe quais serviços existem, quanto custam e quanto duram;
- **Tempo perdido** — horas por dia trocando mensagens para encaixar um atendimento.

O CalendarioServico centraliza o catálogo, a agenda e o histórico em um só lugar, **calcula automaticamente os horários livres** e **impede reservas sobrepostas**.

### Público-alvo

| Público | Necessidade |
|---|---|
| **Prestador de serviço autônomo** | Organizar catálogo, horários de trabalho e atendimentos sem trocar dezenas de mensagens. |
| **Cliente final** | Encontrar um serviço, saber o preço e reservar um horário de forma rápida e transparente. |

---

## 2. Acesso ao aplicativo

### Versão publicada (deploy)

> **Link de acesso:** *a definir* — quando o aplicativo for publicado (por exemplo, no Streamlit Community Cloud), o endereço será informado aqui.

### Orientações de acesso

- Acesse pelo navegador (Chrome, Edge, Firefox ou Safari) em computador ou celular.
- Não é necessário instalar nada: basta **criar uma conta** na tela inicial escolhendo o perfil **Cliente** ou **Prestador** (veja a [seção 5.1](#51-primeiros-passos-todos-os-perfis)).
- Cada conta tem um único perfil. Para testar as duas jornadas, crie duas contas com e-mails diferentes.

### Executando localmente

Enquanto não houver deploy, o aplicativo pode ser executado no próprio computador:

```bash
# 1. Clonar o repositório
git clone https://github.com/thiagotgoncalves-FIT/CalendarioServicos.git
cd CalendarioServicos

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar as variáveis de ambiente
cp .env.example .env
# edite o .env e informe a URL da API do Xano em XANO_API_URL

# 5. Iniciar o aplicativo
streamlit run app.py
```

Depois, abra <http://localhost:8501> no navegador.

> O arquivo `.env` guarda a URL da API e **não deve ser enviado ao GitHub** (ele já está no `.gitignore`).

---

## 3. Perfis de usuários

O aplicativo possui dois perfis, escolhidos no momento do cadastro. Cada usuário vê apenas a área correspondente ao seu perfil e **só acessa os próprios dados**.

### 👤 Cliente

Quem contrata os serviços.

| Pode | Não pode |
|---|---|
| Consultar o catálogo de serviços ativos | Criar ou editar serviços |
| Usar o Assistente de Recomendação | Ver a agenda de outros clientes |
| Agendar um horário livre | Alterar a grade de horários de um prestador |
| Acompanhar e cancelar os próprios agendamentos | Marcar um atendimento como concluído |
| Avaliar atendimentos concluídos (nota de 1 a 5 e comentário) | |
| Editar perfil, foto, tema e senha | |

### 💼 Prestador

O profissional que oferece os serviços.

| Pode | Não pode |
|---|---|
| Cadastrar, desativar e reativar os próprios serviços | Ver ou alterar serviços de outros prestadores |
| Definir a grade semanal de atendimento (dias, horários e pausa) | Agendar serviços como cliente |
| Ver o resumo do dia (métricas e atendimentos de hoje) | Avaliar atendimentos |
| Gerenciar a agenda: filtrar, concluir e cancelar atendimentos | |
| Enviar lembrete ao cliente pelo WhatsApp | |
| Exportar a agenda em CSV | |
| Editar perfil, foto, tema e senha | |

> As regras de autenticação e de acesso por perfil são validadas no backend (Xano), não apenas na tela.

---

## 4. Funcionalidades

### Gerais

- **Cadastro e login** com e-mail e senha (senha guardada com criptografia no backend).
- **Recuperação de senha** com código de verificação de 6 dígitos.
- **Configurações da conta**: foto de perfil, nome, telefone, tema claro/escuro e troca de senha.
- **Menu lateral** com nome, perfil do usuário e atalhos para Início, Ajustes e Sair.

### Prestador

- **Resumo**: agendamentos de hoje, quantidade de serviços ativos, preço médio e receita prevista.
- **Agenda de Atendimentos**: lista de reservas com filtros por status e data, ações de *Concluir* e *Cancelar*, link de lembrete no WhatsApp e exportação em CSV.
- **Meus Serviços**: cadastro de serviços (título, preço, duração e descrição) e ativação/desativação.
- **Grade de Atendimento**: configuração dos dias da semana, horário de início/término e pausa para almoço.

### Cliente

- **Assistente de Recomendação**: indica os profissionais mais adequados com base no serviço procurado, no orçamento máximo e na data desejada, com nota de compatibilidade e justificativas.
- **Catálogo Geral**: todos os serviços ativos, com detalhes, avaliações e agendamento.
- **Cálculo automático de horários livres**: só aparecem horários dentro do expediente, fora da pausa, no futuro e sem conflito com outras reservas.
- **Meus Agendamentos**: histórico com status, cancelamento e avaliação do atendimento.
- **Avaliações**: nota de 1 a 5 estrelas e comentário após o atendimento concluído; a média aparece para outros clientes.

---

## 5. Manual de utilização

> 📸 **Capturas de tela:** as imagens deste manual ficam na pasta [`docs/imagens/`](docs/imagens/).

### 5.1 Primeiros passos (todos os perfis)

#### Passo 1 — Criar uma conta

1. Abra o aplicativo. A tela **Bem-vindo ao AgendAí** é exibida.
2. Clique em **Não tem uma conta? Criar conta**.
3. Preencha o formulário:
   - **Nome Completo / Nome Fantasia**
   - **E-mail**
   - **WhatsApp / Telefone** — com DDD, ex.: `(11) 99999-9999`
   - **Senha** e **Confirmação de Senha** — no mínimo 8 caracteres, com letras e números
4. Em **Qual é o seu perfil de uso?**, escolha:
   - **Cliente** — para agendar serviços; ou
   - **Prestador de Serviços** — para divulgar horários e gerenciar clientes.
5. Clique em **Cadastrar e Começar**.

![Tela de cadastro](docs/imagens/01-cadastro.png)

**Resultado esperado:** a conta é criada e você entra automaticamente no painel do seu perfil. Se o e-mail já estiver cadastrado ou a senha não seguir as regras, uma mensagem de erro explica o que corrigir.

#### Passo 2 — Entrar no aplicativo

1. Na tela inicial, informe **E-mail** e **Senha**.
2. Clique em **Entrar no AgendAí**.

![Tela de login](docs/imagens/02-login.png)

**Resultado esperado:** o painel do seu perfil é aberto. O menu lateral mostra seu nome e o selo **Cliente** ou **Prestador Autônomo**. Com dados incorretos, aparece um aviso de credenciais inválidas.

#### Passo 3 — Recuperar a senha (se necessário)

1. Na tela de login, clique em **Esqueceu sua senha?**.
2. Informe o e-mail cadastrado e clique em **Gerar Código de Verificação**.
3. Um **código de 6 dígitos** é exibido na tela. Digite-o no campo indicado e clique em **Validar Código**.
4. Informe a **Nova Senha**, repita em **Confirme a Nova Senha** e clique em **Redefinir e Salvar Senha**.

**Resultado esperado:** a senha é atualizada e você pode voltar ao login com a nova senha. Use **Recomeçar Recuperação** caso queira reiniciar o processo.

#### Passo 4 — Sair

Clique em **Sair** no menu lateral. A sessão é encerrada e você volta à tela de login.

---

### 5.2 Jornada do Prestador

Sequência recomendada no primeiro uso: **cadastrar serviços → configurar a grade → acompanhar a agenda**. Sem serviços ativos e sem grade configurada, os clientes não conseguem agendar.

O painel do prestador exibe a saudação **Olá, {seu nome}!** e quatro abas: **📊 Resumo**, **📅 Agenda de Atendimentos**, **✂️ Meus Serviços** e **⏰ Grade de Atendimento**.

![Painel do prestador](docs/imagens/03-prestador-resumo.png)

#### Passo 1 — Cadastrar serviços (aba ✂️ Meus Serviços)

1. Abra a aba **✂️ Meus Serviços**.
2. Expanda **Adicionar Novo Serviço**.
3. Preencha:
   - **Título do Serviço** — ex.: *Corte Degradê*
   - **Preço (R$)** — ex.: *45,00*
   - **Duração (minutos)** — em múltiplos de 15, ex.: *30* ou *60*
   - **Breve descrição** (opcional) — ex.: *Corte com acabamento na navalha*
4. Clique em **Salvar Serviço no Catálogo**.

![Cadastro de serviço](docs/imagens/04-prestador-servicos.png)

**Resultado esperado:** uma notificação confirma o cadastro e o serviço aparece em **Seus serviços cadastrados** como ativo, já visível para os clientes no catálogo.

**Desativar ou reativar um serviço:** em cada cartão de serviço, use **Desativar** para tirá-lo do catálogo (ex.: um serviço temporariamente indisponível) e **Reativar** para voltar a oferecê-lo. Serviços desativados não aparecem para os clientes.

#### Passo 2 — Configurar a grade de atendimento (aba ⏰ Grade de Atendimento)

1. Abra a aba **⏰ Grade de Atendimento**. Os sete dias da semana são listados (por padrão, segunda a sexta, das 09:00 às 18:00, com pausa das 12:00 às 13:00).
2. Para cada dia:
   - Marque **Atender neste dia** para habilitá-lo;
   - Ajuste **Início** e **Término** do expediente;
   - Marque **Intervalo / Almoço** e informe **Pausa (Início)** e **Pausa (Fim)**, se houver pausa.
3. Clique em **Salvar Grade de Atendimento**.

![Grade de atendimento](docs/imagens/05-prestador-grade.png)

**Resultado esperado:** a mensagem *"Sua grade de atendimento foi atualizada com sucesso."* é exibida. A partir daí, os horários oferecidos aos clientes seguem essa grade.

**Validações:** o aplicativo não salva a grade se o término for anterior ao início, se o fim da pausa for anterior ao início da pausa ou se a pausa estiver fora do expediente — nesses casos, uma mensagem indica o dia com erro.

#### Passo 3 — Acompanhar o dia (aba 📊 Resumo)

A aba **📊 Resumo** mostra:

- **Agendamentos Hoje** — quantidade de atendimentos marcados para hoje;
- **Serviços Ativos** — quantos serviços estão disponíveis aos clientes;
- **Preço Médio** — média dos serviços ativos e a **receita prevista** (atendimentos confirmados e concluídos);
- **Atendimentos Agendados para Hoje** — lista com serviço, horário, valor e status.

**Resultado esperado:** visão rápida do dia ao abrir o aplicativo. Se não houver atendimentos hoje, aparece a mensagem *"Você ainda não tem agendamentos hoje"*.

#### Passo 4 — Gerenciar a agenda (aba 📅 Agenda de Atendimentos)

1. Abra a aba **📅 Agenda de Atendimentos**.
2. (Opcional) Use os filtros:
   - **Filtrar por Status** — Todos, Confirmado, Pendente, Concluído ou Cancelado;
   - **Filtrar por Data** — mostra apenas um dia específico.
3. Em cada cartão você vê serviço, data e horário, nome do cliente, duração, valor e status.
4. Ações disponíveis para atendimentos **confirmados** ou **pendentes**:
   - **Enviar Lembrete no WhatsApp** — abre o WhatsApp com uma mensagem pronta para o cliente, contendo serviço, data e horário;
   - **Concluir** — marca o atendimento como realizado;
   - **Cancelar** — cancela a reserva e libera o horário.
5. Para baixar a lista filtrada, clique em **Exportar Agenda (CSV)**.

![Agenda de atendimentos](docs/imagens/06-prestador-agenda.png)

**Resultados esperados:**

- Ao **concluir**, o status muda para *Concluído*, o valor entra na receita e o cliente passa a poder avaliar o atendimento.
- Ao **cancelar**, o status muda para *Cancelado* e o horário volta a ficar livre para outros clientes.
- A **exportação** gera o arquivo `agenda_atendimentos_AAAAMMDD.csv`, que abre no Excel ou Google Planilhas.

---

### 5.3 Jornada do Cliente

Sequência típica: **encontrar um serviço → escolher data e horário → confirmar → acompanhar → avaliar**.

O painel do cliente exibe a saudação **Olá, {seu nome}!**, os indicadores **Agendamentos Ativos** e **Total de Agendamentos** e três abas: **🤖 Assistente de Recomendação**, **📖 Catálogo Geral** e **🗓️ Meus Agendamentos**.

![Área do cliente](docs/imagens/07-cliente-painel.png)

#### Passo 1 (opção A) — Encontrar um profissional com o Assistente de Recomendação

Indicado quando você sabe o que precisa, mas não sabe com quem marcar.

1. Abra a aba **🤖 Assistente de Recomendação**.
2. Preencha:
   - **Qual serviço você procura?** — ex.: *Corte de Cabelo*, *Barba*, *Massagem*;
   - **Descreva brevemente sua necessidade** (opcional) — ex.: *corte degradê antes das 18h*;
   - **Orçamento Máximo (R$)** — serviços acima desse valor são descartados;
   - **Data pretendida para o atendimento** — apenas profissionais com vaga nessa data são considerados.
3. Clique em **Encontrar Melhores Recomendações**.

![Assistente de recomendação](docs/imagens/08-cliente-assistente.png)

**Resultado esperado:** uma lista de profissionais ordenada por **nota de compatibilidade**, cada um com preço, duração, os **fatores da recomendação** (ex.: *"Preço favorável"*, *"Excelente disponibilidade"*, *"Alta compatibilidade com a especialidade"*) e a média das avaliações. Para reservar direto daqui, expanda **Reservar Horário com {profissional}**, escolha o horário e clique em **Confirmar Agendamento Imediato**.

Se nada for encontrado, o aplicativo sugere flexibilizar a data ou aumentar o orçamento.

#### Passo 1 (opção B) — Escolher pelo Catálogo Geral

1. Abra a aba **📖 Catálogo Geral**. Cada cartão mostra título, descrição, valor e duração do serviço.
2. (Opcional) Clique em **Detalhes** para ver a nota média e os comentários de outros clientes sobre o serviço.

![Catálogo de serviços](docs/imagens/09-cliente-catalogo.png)

#### Passo 2 — Agendar um horário

1. No cartão do serviço, clique em **Selecionar Horário e Agendar** (ou, na janela de detalhes, expanda **📅 Agendar este Serviço**).
2. Escolha a **Data do Atendimento** (somente hoje ou datas futuras).
3. Em **Horários livres disponíveis**, selecione o horário desejado.
4. Clique em **Confirmar Agendamento**.

![Seleção de horário](docs/imagens/10-cliente-agendar.png)

**Resultado esperado:** a mensagem *"Agendamento confirmado para {data} às {hora}!"* é exibida e a reserva aparece em **Meus Agendamentos**. O horário deixa de ser oferecido a outros clientes.

**Como os horários são calculados:** o aplicativo só exibe horários que estejam dentro do expediente do prestador, fora da pausa para almoço, no futuro e que não se sobreponham a outra reserva, considerando a duração do serviço. Se o dia estiver lotado ou o prestador não atender naquele dia, aparece *"Nenhum horário livre disponível para esta data."* — escolha outra data.

#### Passo 3 — Acompanhar e cancelar agendamentos (aba 🗓️ Meus Agendamentos)

1. Abra a aba **🗓️ Meus Agendamentos**. Cada reserva mostra serviço, data, horário, duração, valor e status.
2. Para desistir de um atendimento **confirmado** ou **pendente**, clique em **Cancelar Agendamento**.

![Meus agendamentos](docs/imagens/11-cliente-meus-agendamentos.png)

**Resultado esperado:** o status passa a *Cancelado* e o horário é liberado na agenda do prestador.

#### Passo 4 — Avaliar o atendimento

Depois que o prestador marca o atendimento como **Concluído**:

1. Ao entrar no aplicativo, um aviso indica que há um atendimento aguardando avaliação e a janela de avaliação é aberta automaticamente. Você também pode clicar em **Avaliar Atendimento** no cartão da reserva em **Meus Agendamentos**.
2. Escolha a **nota de 1 a 5 estrelas** e, se quiser, escreva um comentário.
3. Clique em **Enviar Avaliação** (ou **Avaliar Mais Tarde** para adiar).

![Avaliação do atendimento](docs/imagens/12-cliente-avaliacao.png)

**Resultado esperado:** o cartão passa a exibir o selo **★ Avaliado (nota/5)** e sua avaliação entra na média do serviço, visível para outros clientes em **Detalhes** e no Assistente de Recomendação. Cada atendimento pode ser avaliado uma única vez.

---

### 5.4 Configurações da conta (todos os perfis)

Acesse pelo botão **⚙️ Ajustes** no menu lateral ou **⚙️ Configurações** no topo do painel. Para retornar, use **⬅️ Voltar** ou **🏠 Início**.

![Configurações da conta](docs/imagens/13-configuracoes.png)

| Aba | O que fazer | Resultado esperado |
|---|---|---|
| **👤 Perfil e Foto** | Envie uma imagem e clique em **Salvar Nova Foto** (ou **Remover Foto**). Altere **Nome Completo** e **Telefone com DDD** e clique em **Salvar Alterações Cadastrais**. O e-mail não pode ser alterado. | Foto e dados atualizados no menu lateral e nos agendamentos. |
| **🎨 Aparência (Tema)** | Escolha **Claro** ou **Escuro** e clique em **Aplicar Preferência de Tema**. | A interface muda de cores; a preferência fica salva na sua conta. |
| **🔒 Segurança e Senha** | Informe **Senha Atual**, **Nova Senha** e **Confirmação da Nova Senha** e clique em **Atualizar Senha**. | Mensagem *"Senha alterada com sucesso!"*; use a nova senha no próximo login. |

---

## 6. Exemplos de utilização

Os cenários abaixo usam dados de demonstração e mostram o aplicativo funcionando de ponta a ponta. Para reproduzi-los, crie **uma conta de Prestador** e **uma conta de Cliente** (com e-mails diferentes).

### Dados de demonstração sugeridos

| Perfil | Nome | E-mail | Telefone | Senha |
|---|---|---|---|---|
| Prestador | Barbearia do Lucas | `lucas.barbeiro@exemplo.com` | (11) 98888-1111 | `Teste1234` |
| Cliente | Maria Souza | `maria.cliente@exemplo.com` | (11) 97777-2222 | `Teste1234` |

> Use apenas dados fictícios. Os e-mails acima são exemplos: se já estiverem cadastrados, escolha outros.

**Serviços do prestador** (os mesmos usados nos dados de demonstração do sistema):

| Serviço | Descrição | Preço | Duração |
|---|---|---|---|
| Corte Masculino & Barba | Corte degradê e alinhamento de barba na navalha | R$ 60,00 | 45 min |
| Barboterapia Relaxante | Toalha quente, massagem facial e hidratação da barba | R$ 40,00 | 30 min |

**Grade de atendimento:** segunda a sexta, das 09:00 às 18:00, com pausa das 12:00 às 13:00; sábado, das 09:00 às 14:00, sem pausa; domingo sem atendimento.

### Cenário 1 — Prestador prepara a agenda

1. Lucas cria a conta como **Prestador** e cadastra os dois serviços em **✂️ Meus Serviços**.
2. Em **⏰ Grade de Atendimento**, configura a grade acima e salva.
3. Na aba **📊 Resumo**, vê **Serviços Ativos = 2** e **Preço Médio = R$ 50,00**.

**Resultado:** os dois serviços passam a aparecer no **Catálogo Geral** de qualquer cliente.

### Cenário 2 — Cliente agenda pelo catálogo

1. Maria entra como **Cliente**, abre **📖 Catálogo Geral** e escolhe **Corte Masculino & Barba**.
2. Em **Selecionar Horário e Agendar**, escolhe uma **quarta-feira** futura.
3. A lista de horários livres começa em `09:00` e avança de 30 em 30 minutos. Os horários que fariam o atendimento de 45 min invadir a pausa (`11:30`) ou passar do fim do expediente não aparecem.
4. Ela seleciona `10:00` e clica em **Confirmar Agendamento**.

**Resultado:** a mensagem *"Agendamento confirmado para {data} às 10:00!"* aparece e a reserva surge em **🗓️ Meus Agendamentos** como *Confirmado*.

### Cenário 3 — Proteção contra conflito de horário

1. Um segundo cliente tenta agendar o mesmo serviço na mesma quarta-feira.
2. Os horários `09:30`, `10:00` e `10:30` **não aparecem mais**, porque se sobreporiam ao atendimento de Maria (10:00–10:45). Os horários `09:00` e `11:00` continuam disponíveis.

**Resultado:** é impossível marcar dois clientes no mesmo horário (*anti-double-booking*).

### Cenário 4 — Cliente usa o Assistente de Recomendação

1. Maria abre **🤖 Assistente de Recomendação** e preenche:
   - **Serviço:** `barba`
   - **Necessidade:** `quero relaxar e hidratar a barba`
   - **Orçamento Máximo:** `R$ 50,00`
   - **Data:** uma sexta-feira futura
2. Clica em **Encontrar Melhores Recomendações**.

**Resultado:** aparece **Barboterapia Relaxante (R$ 40,00)** com justificativas como *"Preço favorável (R$ 10,00 abaixo do seu orçamento)"*. O **Corte Masculino & Barba (R$ 60,00)** não aparece, porque passa do orçamento.

### Cenário 5 — Prestador conclui o atendimento e o cliente avalia

1. Lucas abre **📅 Agenda de Atendimentos**, filtra pela data do atendimento e clica em **Enviar Lembrete no WhatsApp**. O WhatsApp abre com uma mensagem pronta para Maria.
2. Após o atendimento, Lucas clica em **Concluir**. O status passa a *Concluído* e o valor entra na receita prevista do **Resumo**.
3. Lucas clica em **Exportar Agenda (CSV)** e abre o arquivo no Excel.
4. No próximo acesso, Maria vê o aviso de atendimento aguardando avaliação, dá **5 estrelas** e escreve *"Ótimo atendimento!"*.

**Resultado:** o cartão do agendamento exibe **★ Avaliado (5/5)** e a nota passa a aparecer em **Detalhes** do serviço para outros clientes.

### Cenário 6 — Cancelamento libera o horário

1. Maria cancela um agendamento futuro em **🗓️ Meus Agendamentos** → **Cancelar Agendamento**.
2. Outro cliente consulta a mesma data.

**Resultado:** o horário cancelado volta a aparecer como livre, e na agenda do prestador a reserva aparece como *Cancelado*.

---

## 7. Limitações conhecidas

Esta seção mostra com transparência o estágio atual da versão entregue.

### Acesso e publicação

- **Sem deploy público até o momento:** o aplicativo precisa ser executado localmente (veja a [seção 2](#2-acesso-ao-aplicativo)) até que um link de publicação seja informado.
- **Sem perfil de Administrador:** não há painel para gestão global de usuários, métricas da plataforma ou moderação de avaliações. Esse perfil está previsto apenas como evolução futura.
- **Um perfil por conta:** um mesmo e-mail não pode ser Cliente e Prestador ao mesmo tempo, e o perfil escolhido no cadastro não pode ser alterado depois.

### Persistência de dados

- **Autenticação (cadastro, login e perfil do usuário)** é feita pelo backend Xano.
- **Catálogo, grade de horários e agendamentos** dependem de endpoints REST do Xano. Quando esses endpoints não respondem, o aplicativo usa um **modo de contingência em memória**: os dados ficam disponíveis enquanto o aplicativo está aberto, mas **são perdidos quando o servidor do Streamlit é reiniciado**.
- **Avaliações, foto de perfil, telefone formatado e senhas alteradas** pelas telas de configuração/recuperação ficam salvos em **arquivos locais** na pasta `uploads/` do servidor, e não no banco do Xano. Em um deploy em nuvem com disco temporário, esses dados podem se perder.

### Funcionalidades

- **Recuperação de senha sem e-mail:** o código de 6 dígitos é exibido na própria tela, e não enviado por e-mail ou SMS. Funciona para demonstração, mas não é um mecanismo seguro para produção.
- **Sem notificações automáticas:** não há envio automático de e-mail, SMS ou WhatsApp. O lembrete pelo WhatsApp é aberto manualmente pelo prestador, com uma mensagem pronta.
- **Agendamento já nasce confirmado:** a reserva do cliente é confirmada na hora. O prestador não tem etapa de aprovação: ele só pode concluir ou cancelar.
- **Sem reagendamento:** para trocar data ou horário, é preciso cancelar e agendar de novo.
- **Serviços não podem ser editados nem excluídos:** só dá para cadastrar, desativar e reativar. Para mudar preço ou duração, cadastre um novo serviço e desative o antigo.
- **Horários em intervalos fixos de 30 minutos:** os horários de início são oferecidos de 30 em 30 minutos, independentemente da duração do serviço.
- **Grade semanal fixa:** não é possível bloquear datas específicas (feriados, férias, folgas pontuais). O bloqueio vale para o dia da semana inteiro.
- **Um prestador por atendimento, sem múltiplos profissionais:** não há gestão de equipe, salas ou recursos compartilhados.
- **Catálogo sem busca ou filtros:** a aba **Catálogo Geral** lista todos os serviços ativos. A busca por termo, preço e data só existe no **Assistente de Recomendação**.
- **Sem pagamentos online:** o valor exibido é informativo; o pagamento é combinado diretamente entre cliente e prestador.
- **Fuso horário único:** datas e horários usam o relógio do servidor, sem tratamento de fusos diferentes.

### Interface

- **Assistente de Recomendação baseado em regras**, e não em inteligência artificial generativa: a pontuação combina palavras-chave, orçamento, quantidade de horários livres e avaliações.
- **Uso em celular:** a interface funciona no navegador do celular, mas foi pensada primeiro para telas de computador; algumas tabelas e grades podem exigir rolagem.

---

## 8. Ciclo de vida de um agendamento

```text
  Cliente agenda
        │
        ▼
 ┌──────────────┐   Prestador conclui   ┌──────────────┐   Cliente avalia
 │  Confirmado  │ ────────────────────▶ │  Concluído   │ ─────────────────▶ ★ Avaliado
 │  / Pendente  │                       └──────────────┘
 └──────────────┘
        │  Cliente ou prestador cancela
        ▼
 ┌──────────────┐
 │  Cancelado   │  (horário volta a ficar livre)
 └──────────────┘
```

| Status | Significado | Quem altera |
|---|---|---|
| **Pendente / Confirmado** | Reserva ativa, aguardando o atendimento. | Criado pelo cliente ao agendar. |
| **Concluído** | Atendimento realizado; entra na receita e libera a avaliação. | Prestador. |
| **Cancelado** | Reserva desfeita; o horário fica livre novamente. | Cliente ou prestador. |

---

## 9. Mensagens comuns e solução de problemas

| Situação | Causa provável | O que fazer |
|---|---|---|
| *"Nenhum horário livre disponível para esta data."* | Dia lotado, data em que o prestador não atende ou horários já passados. | Escolha outra data. |
| *"Nenhum serviço ativo disponível"* no catálogo | Nenhum prestador cadastrou ou ativou serviços. | Prestador: cadastre ou reative um serviço em **Meus Serviços**. |
| Erro ao cadastrar: e-mail já em uso | Já existe uma conta com esse e-mail. | Faça login ou use **Esqueceu sua senha?**. |
| Erro ao cadastrar ou trocar senha | Senha com menos de 8 caracteres ou sem letras e números. | Crie uma senha com pelo menos 8 caracteres, misturando letras e números. |
| Credenciais inválidas no login | E-mail ou senha incorretos. | Confira os dados ou recupere a senha. |
| Erro ao salvar a grade | Término antes do início ou pausa fora do expediente. | Corrija os horários do dia indicado na mensagem. |
| Botão **Exportar Agenda (CSV)** desabilitado | Nenhum atendimento para os filtros escolhidos. | Ajuste os filtros de status ou data. |
| Link do WhatsApp não aparece | O cliente não informou telefone válido. | Peça ao cliente para atualizar o telefone em **Configurações**. |

---

## 10. Informações técnicas

| Camada | Tecnologia |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) (Python) |
| Backend e banco de dados | [Xano](https://www.xano.com/) — APIs REST, autenticação por token e regras em XanoScript |
| Metodologia | [OpenSpec](https://openspec.dev/) — desenvolvimento orientado a especificações (*Explore → Propose → Review → Apply → Archive*) |

Documentação complementar para desenvolvedores:

- [`docs/project-overview.md`](docs/project-overview.md) — visão geral, escopo e roadmap;
- [`docs/domain-model.md`](docs/domain-model.md) — modelo de domínio e regras de negócio;
- [`openspec/specs/`](openspec/specs/) — especificações de cada funcionalidade;
- [`CHANGELOG.md`](CHANGELOG.md) — histórico de versões;
- [`AGENTS.md`](AGENTS.md) — regras de desenvolvimento com IA.

### Testes automatizados

```bash
python test_roles_isolation.py        # autenticação e isolamento de perfis
python test_appointment_engine.py     # cálculo de horários e anti-double-booking
python test_recommendation_engine.py  # assistente de recomendação
python test_review_system.py          # sistema de avaliações
python test_user_settings.py          # configurações da conta
```

---

<sub>Projeto acadêmico — Faculdade IMPACTA · Innovation Lab: Advanced No/Low Code · 2026</sub>
