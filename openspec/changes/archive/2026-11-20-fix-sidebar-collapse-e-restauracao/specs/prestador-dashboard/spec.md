## MODIFIED Requirements

### Requirement: Cabeçalho Contextual e Boas-Vindas
O sistema MUST exibir no cabeçalho do painel uma saudação personalizada utilizando o nome real do usuário autenticado na sessão (`st.session_state["user"]`), acompanhado do nome da plataforma, perfil de acesso e da data corrente por extenso em português do Brasil (ex.: "18 de outubro de 2026"). Na barra lateral esquerda, o sistema MUST posicionar o bloco de identificação do usuário logado (avatar, nome, e-mail e badge de perfil) logo no topo superior e MUST garantir que, mesmo quando recolhida, a barra lateral permaneça acessível através de ícones ou controle visível de expansão.

#### Scenario: Visualização do Cabeçalho por Prestador Autenticado
- **WHEN** o prestador Hector Barros acessa o painel autenticado
- **THEN** o sistema exibe saudação nominal baseada em seu registro de usuário e a data de hoje formatada em pt-BR

#### Scenario: Layout Compacto Superior do Perfil na Barra Lateral
- **WHEN** qualquer usuário (prestador ou cliente) estiver autenticado
- **THEN** a barra lateral esquerda apresenta a marca do AgendAí e o cartão de identificação do usuário no topo superior, garantindo acesso direto e visibilidade imediata sem necessidade de rolagem

#### Scenario: Preservação de Ícones e Controle de Expansão ao Recolher Barra Lateral
- **WHEN** o usuário aciona o recolhimento da barra lateral
- **THEN** a barra lateral não desaparece sem controle de retorno: o sistema mantém acessível o botão de alternância de expansão e preserva acesso visual aos ícones principais (avatar/marca e configurações)
