# Design: Persistência Durável de Avaliações e Bloqueio de Reavaliação

## 1. Arquitetura da Solução

O sistema adotará armazenamento local baseado em arquivos JSON no diretório de persistência durável `uploads/`, replicando o padrão seguro já utilizado com sucesso para fotos de perfil e credenciais de login (`uploads/user_credentials.json`).

### 1.1 Arquivos de Armazenamento
- `uploads/reviews.json`: Armazena a lista completa de avaliações (incluindo as avaliações seminais/iniciais e todas as submetidas pelos usuários).
- `uploads/reviewed_appointments.json`: Armazena a lista de IDs de agendamentos (`agendamento_id`) já avaliados como strings para busca imediata em $O(1)$ ou $O(N)$ em memória.

### 1.2 Estrutura de Dados em `uploads/reviews.json`
```json
[
  {
    "id": 1,
    "agendamento_id": "991",
    "cliente_id": "101",
    "prestador_id": "15",
    "servico_id": "1",
    "servico_titulo": "Corte Masculino & Barba",
    "cliente_nome_exibicao": "Camila R.",
    "nota": 5,
    "comentario": "Excelente atendimento! O profissional foi super pontual e o corte ficou impecável. Recomendo muito!",
    "criado_em": "2026-10-28 14:30:00"
  }
]
```

### 1.3 Estrutura de Dados em `uploads/reviewed_appointments.json`
```json
[
  "991",
  "992",
  "993"
]
```

## 2. Modificações em Módulos

### 2.1 `services/review_service.py`
1. **Funções Auxiliares de I/O Seguro**:
   - `_load_persisted_reviews() -> List[Dict[str, Any]]`: Garante a existência do arquivo `uploads/reviews.json`. Caso não exista, inicializa com `MOCK_REVIEWS` default e persiste.
   - `_save_persisted_reviews(reviews: List[Dict[str, Any]]) -> None`: Grava atômica/seguramente a lista no arquivo JSON.
   - `_load_reviewed_appointments() -> List[str]`: Carrega a lista de IDs de agendamentos avaliados de `uploads/reviewed_appointments.json`.
   - `_mark_appointment_persisted_reviewed(agendamento_id: Union[int, str]) -> None`: Adiciona o `agendamento_id` convertido para string ao arquivo de agendamentos avaliados caso ainda não conste.
2. **`is_appointment_reviewed(agendamento_id, token=None) -> bool`**:
   - Verifica primeiro se o ID consta no arquivo persistido `uploads/reviewed_appointments.json` ou em `uploads/reviews.json`.
   - Se constar, retorna `True` imediatamente (não reabre modal).
   - Se não constar, consulta a API Xano (se disponível); se a API retornar positivo, também grava no arquivo persistido local.
3. **`submit_review(...)`**:
   - Ao receber a submissão, cria o payload com `servico_id` validado.
   - Mesmo que a API Xano retorne erro ou sucesso, insere o registro no arquivo persistido `uploads/reviews.json` e marca o `agendamento_id` em `uploads/reviewed_appointments.json`.
   - Dispara `appointment_service.mark_appointment_reviewed(agendamento_id)`.
4. **`get_reviews(...)`**:
   - Carrega as avaliações do arquivo persistido `uploads/reviews.json` quando em modo local/fallback ou quando a consulta à API retornar vazio/falhar.
   - Aplica os filtros contextuais por `servico_id` e `prestador_id`.
   - Ordena da mais recente para a mais antiga (`criado_em`).
5. **`get_metrics(...)`**:
   - Baseia-se no resultado de `get_reviews(...)`, garantindo que notas submetidas recalculem instantaneamente a média e o total de avaliações do serviço.

### 2.2 `services/appointment_service.py`
- Sincroniza `mark_appointment_reviewed(appointment_id)` com `review_service.mark_appointment_persisted_reviewed(appointment_id)` para garantir persistência bidirecional.
- Na verificação de agendamentos (`get_appointments_by_user` e `get_appointment_by_id`), enriquece os registros com o campo booleano `avaliado = review_service.is_appointment_reviewed(app_id)`.

### 2.3 `app.py`
- Em `show_review_appointment_dialog`, após `submit_review`, persiste o status na sessão e garante que o modal feche e `apps_pendentes_avaliacao` não selecione mais o mesmo agendamento.
- Em `show_service_details_dialog`, a chamada a `review_service.get_reviews(servico_id=s_id)` exibirá imediatamente a avaliação recém-gravada no JSON em disco.
