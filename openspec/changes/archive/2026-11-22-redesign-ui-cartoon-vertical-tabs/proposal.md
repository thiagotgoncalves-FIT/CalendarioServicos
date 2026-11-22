# Proposta: Redesign Visual com Abas Verticais, Ícones e Tipografia Cartoon

## 1. Contexto e Motivação

O usuário solicitou uma modernização visual do aplicativo com quatro pilares centrais:
1. **Visual mais limpo**: Remoção de poluição visual, espaçamentos generosos (padding/margins) e acabamentos suaves.
2. **Ícones ao lado dos nomes das abas**: Incorporação de ícones representativos em cada aba de navegação (ex.: 📊 Resumo, 📅 Agenda, ✂️ Serviços, ⏰ Grade de Horários, 🤖 Assistente, 📖 Catálogo, 🗓️ Meus Agendamentos, 👤 Perfil, 🎨 Aparência, 🔒 Segurança).
3. **Abas na vertical**: Disposição das abas em formato vertical / coluna lateral estilizada, permitindo navegação ergonômica, fluida e moderna.
4. **Tipografia Cartoon & Destaques em Negrito**:
   - Tipografia arredondada com estética amigável/cartoon (Google Font `Fredoka` e `Quicksand`), trazendo identidade visual descontraída e agradável.
   - Destaque em **negrito marcante (`font-weight: 800` / `900`)** para dados importantes: preços de serviços, status de agendamentos, notas de avaliações, métricas e títulos principais.

## 2. Escopo da Mudança

- **Módulo de Estilos Globais (`services/ui_utils.py`)**:
  - Injeção das fontes Google Fonts (`Fredoka:wght@400;600;700;800` e `Quicksand:wght@500;700`).
  - Aplicação universal da tipografia cartoon arredondada em todos os títulos, textos, botões e cartões.
  - Estilização universal de destaques em negrito (preços, status, notas e totais).
  - Regras CSS avançadas para suportar a apresentação de abas/navegação na vertical com botões arredondados, bordas sutis e estados ativos nítidos.
- **Interface Principal (`app.py`)**:
  - Atualização dos rótulos de abas adicionando ícones expressivos e contextuais em:
    - **Área do Prestador**: `["📊 Resumo", "📅 Agenda de Atendimentos", "✂️ Meus Serviços", "⏰ Grade de Atendimento"]`
    - **Área do Cliente**: `["🤖 Assistente de Recomendação", "📖 Catálogo Geral", "🗓️ Meus Agendamentos"]`
    - **Configurações da Conta**: `["👤 Perfil e Foto", "🎨 Aparência (Tema)", "🔒 Segurança e Senha"]`
  - Estruturação do layout das abas verticais através de container/colunas com navegação em formato vertical estilizado ou injeção CSS específica de abas verticais.
  - Reforço visual em negrito para os pontos vitais de dados (valores em R$, status concluído/confirmado/pendente, avaliações ★).
- **Compatibilidade e Integridade**:
  - Manter funcionamento impecável em ambos os temas (**Claro** e **Escuro**).
  - Manter intactas todas as regras de negócio, testes e formulários.
