from services import catalog_service, availability_service

print("--- Testando Catalog Service ---")
sucesso, servicos = catalog_service.get_services(prestador_id=1)
print(f"Sucesso ao buscar: {sucesso}")
print(f"Serviços encontrados: {len(servicos)}")
print(f"Primeiro serviço: {servicos[0]['titulo']} - R${servicos[0]['preco']}")

print("\nAdicionando um novo serviço...")
sucesso, novo_servico = catalog_service.create_service(prestador_id=1, titulo="Corte Infantil", preco=25.0, duracao_minutos=30)
print(f"Sucesso ao adicionar: {sucesso}")
print(f"Serviço adicionado: {novo_servico['titulo']} - R${novo_servico['preco']} (ID: {novo_servico['id']})")

print("\nListando novamente...")
_, servicos_atualizados = catalog_service.get_services(prestador_id=1)
print(f"Serviços encontrados: {len(servicos_atualizados)}")

print("\n--- Testando Availability Service ---")
sucesso, grade = availability_service.get_availability(prestador_id=1)
print(f"Sucesso ao buscar grade: {sucesso}")
print(f"Dias na grade: {len(grade)}")
print(f"Segunda-feira (dia 1): {next(d for d in grade if d['dia_semana'] == 1)}")

print("\nAtualizando grade...")
grade[0]["hora_inicio"] = "08:00" # Atualiza segunda-feira
sucesso, response = availability_service.save_availability(prestador_id=1, schedule_data=grade)
print(f"Sucesso ao salvar grade: {sucesso}")
print(f"Resposta: {response['message']}")
