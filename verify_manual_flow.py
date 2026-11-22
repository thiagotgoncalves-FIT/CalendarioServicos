from services import auth_service, catalog_service, availability_service, appointment_service, review_service, ui_utils

print("=== 1. PRESTADOR E CLIENTE EXISTENTES ===")
# Hector como prestador (id=15)
_, hector_session = auth_service.login("hector.barros@aluno.impacta.edu.br", "123")
token_hector = hector_session["authToken"]
print("Hector (Prestador) logado:", hector_session["user"]["name"], hector_session["user"]["role"])

# Mariana como cliente (id=2)
_, mariana_session = auth_service.login("mariana@email.com", "123")
token_mariana = mariana_session["authToken"]
print("Mariana (Cliente) logada:", mariana_session["user"]["name"], mariana_session["user"]["role"])

print("\n=== 2. CLIENTE AGENDA SERVIÇO ===")
data_teste = "2026-11-20"
hora_teste = "14:00"
suc_ag, app = appointment_service.create_appointment(
    cliente_id=mariana_session["user"]["id"],
    prestador_id=15,
    servico_id=1,
    data_str=data_teste,
    hora_inicio=hora_teste,
    token=token_mariana,
    cliente_nome=mariana_session["user"]["name"],
    cliente_telefone=mariana_session["user"]["phone"]
)
assert suc_ag is True
app_id = app["id"]
print(f"Agendamento #{app_id} criado para {data_teste} às {hora_teste} com status: {app.get('status')}")

print("\n=== 3. PRESTADOR FINALIZA ATENDIMENTO ===")
suc_fin, app_fin = appointment_service.update_appointment_status(app_id, "concluido", token=token_hector)
assert suc_fin is True
print(f"Atendimento #{app_id} atualizado pelo prestador para: {app_fin.get('status')}")

print("\n=== 4. CLIENTE AVALIA O ATENDIMENTO ===")
# Verificação de elegibilidade antes
assert review_service.is_appointment_reviewed(app_id) is False
suc_rev, resp_rev = review_service.submit_review(
    agendamento_id=app_id,
    cliente_id=mariana_session["user"]["id"],
    prestador_id=15,
    nota=5,
    comentario="Atendimento sensacional pelo Hector! Muito caprichoso.",
    cliente_nome=mariana_session["user"]["name"],
    servico_id=app_fin.get("servico_id"),
    servico_titulo=app_fin.get("servico_titulo"),
    token=token_mariana
)
assert suc_rev is True, f"Erro no submit_review: {resp_rev}"
print("Avaliação registrada com sucesso! ID:", resp_rev.get("id"), "Nota:", resp_rev.get("nota"))

print("\n=== 5. OUTRO CLIENTE OU VISITANTE VÊ NOS DETALHES DO SERVIÇO ===")
metrics = review_service.get_metrics(servico_id=1)
print(f"Métricas atualizadas do Serviço #1: Média {metrics['nota_media']} ★ ({metrics['total_avaliacoes']} avaliações)")

_, reviews_serv = review_service.get_reviews(servico_id=1)
ultima_rev = reviews_serv[0]
print(f"Depoimento visível para outro cliente: \"{ultima_rev['comentario']}\"")
print(f"Autor visível com privacidade: {ultima_rev['cliente_nome_exibicao']}")
print(f"Nota: {ultima_rev['nota']} estrelas")

assert str(ultima_rev.get("agendamento_id")) == str(app_id)
assert ultima_rev["nota"] == 5
assert review_service.is_appointment_reviewed(app_id) is True
print("\n[VERIFICAÇÃO MANUAL COMPLETA: 100% DE SUCESSO]")
