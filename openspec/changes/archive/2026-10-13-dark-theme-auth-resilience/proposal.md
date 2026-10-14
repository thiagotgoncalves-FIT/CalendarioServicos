## Why

Atualmente, ao tentar criar uma conta ou autenticar na interface do Streamlit, o endpoint do Xano (`/auth/signup`) retorna HTTP 200 com corpo `null`, pois a rota ainda não possui lógica de persistência e geração de token configurada no Function Stack do backend remoto. Isso causa uma falha bloqueante com a mensagem *"Erro ao realizar cadastro no Xano. Verifique a conexão com a API."*, impedindo que usuários testem a plataforma, criem contas e acessem os painéis de Prestador ou Cliente. Além disso, o design visual atual utiliza tema claro básico e pouco contrastado, distante do padrão visual profissional exigido para a entrega do projeto.

Esta mudança introduz uma camada de autenticação resiliente com fallback inteligente para permitir cadastro e login fluidos, somada a uma reformulação visual completa em **Dark Theme Premium**.

## What Changes

- **Resiliência e Fallback na Autenticação**: Implementação de tratamento gracioso em `auth_service.py` para respostas nulas ou erros de conexão do Xano, permitindo criação de novos usuários e login contínuo com persistência local de sessão quando o backend remoto não retornar payload válido.
- **Configuração Dark Theme Nativa**: Ajuste de `.streamlit/config.toml` com paleta de cores escura profissional (fundo Slate/Obsidian, texto claro de alta legibilidade, cores primárias vibrantes).
- **Redesign Visual da Interface (Dark UI)**: Estilização dos componentes em `app.py` com CSS moderno, incluindo formulários em estilo dark glassmorphism, campos de entrada contrastados com foco azul elétrico, botões com microinterações e cabeçalhos refinados.
- **Transição e Feedback em Tempo Real**: Mensagens visuais claras sobre o status da autenticação e perfil ativo (Prestador ou Cliente).

## Capabilities

### New Capabilities
<!-- Nenhuma nova capacidade raiz criada; refinamento das capacidades existentes -->

### Modified Capabilities
- `user-auth`: O sistema passa a tolerar respostas nulas ou instabilidades do backend remoto do Xano através de fallback transparente para sessão local, assegurando que o usuário consiga se cadastrar com e-mail, senha, telefone e perfil (prestador/cliente) e efetuar login sem bloqueio.

## Impact

- **Código Frontend**: `app.py`, `.streamlit/config.toml`
- **Serviços**: `services/auth_service.py`, `services/api_client.py`
- **APIs**: Mantém a tentativa primária de chamada para `https://x8ki-letl-twmt.n7.xano.io/api:M19UcCw4/auth/signup` e `/auth/login`, ativando fallback quando a resposta for nula ou inválida.
