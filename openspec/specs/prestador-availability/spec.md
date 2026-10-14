# prestador-availability Specification

## Purpose
Permitir que o prestador de serviços configure seus dias e intervalos de funcionamento semanal, estabelecendo os limites de horário de início, término e pausas de atendimento.

## Requirements

### Requirement: Parametrização da Grade Semanal
O prestador autenticado DEVE conseguir definir em quais dias da semana realiza atendimentos (Segunda a Domingo) e estipular o horário de abertura e fechamento para cada dia ativo.

#### Scenario: Ativação de Dia de Atendimento com Horários Válidos
- **WHEN** o prestador habilita a "Segunda-feira" com expediente das 09:00 às 18:00 e pausa das 12:00 às 13:00
- **THEN** o sistema salva a configuração da grade para aquele dia associada ao prestador

#### Scenario: Validação de Ordem Cronológica de Expediente
- **WHEN** o prestador configura um horário de término anterior ou igual ao horário de início
- **THEN** o sistema recusa a configuração e exibe mensagem informando que o horário de término deve ser posterior ao início

#### Scenario: Validação de Intervalo de Almoço/Pausa
- **WHEN** o prestador configura um intervalo de pausa fora da janela de expediente (ex: intervalo às 19:00 com expediente encerrando às 18:00)
- **THEN** o sistema sinaliza que o intervalo de repouso deve ocorrer dentro do período de funcionamento

---

### Requirement: Consulta da Grade pelo Prestador
O sistema DEVE carregar a grade semanal previamente configurada ao acessar a tela de horários.

#### Scenario: Carregamento dos Horários Salvos
- **WHEN** o prestador acessa a aba de horários de trabalho
- **THEN** o sistema apresenta a grade com os dias selecionados e seus respectivos horários preenchidos
