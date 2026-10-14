## Why

O frontend atual no Streamlit possui um visual muito básico e precisa evoluir para entregar a experiência de uma plataforma SaaS profissional para os prestadores. Além disso, a autenticação está dependendo de dados em memória (mock) caso o backend não esteja configurado corretamente, impedindo que os novos usuários criados sejam persistidos em um banco de dados real no Xano e que o fluxo de login funcione de ponta a ponta.

## What Changes

- Implementação de injeção de CSS e ajustes de layout no `app.py` para criar uma interface mais limpa, profissional e com micro-interações.
- Ajuste e validação do serviço de autenticação (`services/auth_service.py`) para garantir a persistência real da criação de usuário (`signup`) no Xano (tabelas `user` e `cliente`).
- Ajuste e validação do fluxo de `login` para recuperar adequadamente os tokens JWT fornecidos pelo Xano.
- Remoção ou desativação de fluxos mockados que mascaram a falta de conexão com o banco de dados.

## Capabilities

### New Capabilities
Nenhuma.

### Modified Capabilities
- `user-auth`: A autenticação (cadastro e login) passa a exigir obrigatoriamente a comunicação em tempo real com o backend no Xano, eliminando o bypass para mocks em memória na estrutura principal de operação.

## Impact

- `app.py`: Ajustes profundos na aparência visual e injeção de estilo customizado.
- `services/auth_service.py`: Refatoração para lidar exclusivamente com chamadas à API real.
- Sistema de Configuração: O `.env` precisará ser configurado adequadamente com a `XANO_API_URL` do banco real para testar o fluxo completo.
