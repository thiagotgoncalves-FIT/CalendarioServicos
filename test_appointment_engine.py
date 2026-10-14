"""
Script de testes automatizados para o Motor de Agendamentos (AgendAí).
Valida cálculo de slots livres, prevenção de conflito/double-booking,
criação de reservas e ciclo de vida de status.
"""

import sys
from datetime import date, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from services import appointment_service, catalog_service, availability_service


def run_tests():
    print("==================================================")
    print("[TEST] INICIANDO TESTES DO MOTOR DE AGENDAMENTOS")
    print("==================================================")

    prestador_id = 1
    cliente_id = 99
    
    # 1. Configuração da data de teste (Próxima quinta-feira para garantir dia de semana com expediente)
    hoje = date.today()
    dias_para_quinta = (3 - hoje.weekday()) % 7
    if dias_para_quinta == 0:
        dias_para_quinta = 7
    data_teste = (hoje + timedelta(days=dias_para_quinta)).strftime("%Y-%m-%d")
    print(f"[*] Data selecionada para o teste: {data_teste}")

    # 2. Teste de cálculo de slots livres
    slots_30m = appointment_service.calculate_available_slots(
        prestador_id=prestador_id,
        date_str=data_teste,
        duration_minutes=30
    )
    print(f"[1] Slots livres gerados (30 min): {len(slots_30m)} horários disponíveis")
    assert len(slots_30m) > 0, "Deveria haver slots livres gerados para dia útil!"
    assert "09:00" in slots_30m, "09:00 deveria estar disponível no início do expediente!"
    assert "12:00" not in slots_30m, "12:00 não pode estar disponível (intervalo de almoço)!"
    assert "12:30" not in slots_30m, "12:30 não pode estar disponível (intervalo de almoço)!"
    print("    [PASS] Teste 1 APROVADO: Cálculo de slots respeita expediente e almoço.")

    # 3. Teste de criação de agendamento válido
    slot_escolhido = slots_30m[0]
    suc, app = appointment_service.create_appointment(
        cliente_id=cliente_id,
        prestador_id=prestador_id,
        servico_id=1,
        data_str=data_teste,
        hora_inicio=slot_escolhido
    )
    assert suc is True, f"Falha ao criar agendamento: {app}"
    assert app.get("status") == "confirmado", "Status inicial deveria ser 'confirmado'!"
    app_id = app.get("id")
    print(f"[2] Agendamento #{app_id} criado para às {slot_escolhido} com status '{app.get('status')}'.")
    print("    [PASS] Teste 2 APROVADO: Agendamento criado com sucesso.")

    # 4. Teste de Prevenção de Duplo Agendamento (Anti-Double-Booking)
    # Tentar agendar no mesmo slot ocupado
    suc_colisao, resp_colisao = appointment_service.create_appointment(
        cliente_id=cliente_id + 1,
        prestador_id=prestador_id,
        servico_id=1,
        data_str=data_teste,
        hora_inicio=slot_escolhido
    )
    assert suc_colisao is False, "Sistema permitiu double-booking indevidamente!"
    print(f"[3] Anti-double-booking: Bloqueou tentativa concorrente com mensagem: '{resp_colisao.get('message')}'.")
    print("    [PASS] Teste 3 APROVADO: Prevenção de conflito de horário funcionando.")

    # 5. Teste de recuperação de agendamentos por perfil
    suc_cli, apps_cli = appointment_service.get_appointments_by_user(cliente_id, role="cliente")
    assert suc_cli is True and any(a["id"] == app_id for a in apps_cli), "Agendamento não encontrado para o cliente!"

    suc_prest, apps_prest = appointment_service.get_appointments_by_user(prestador_id, role="prestador")
    assert suc_prest is True and any(a["id"] == app_id for a in apps_prest), "Agendamento não encontrado para o prestador!"
    print(f"[4] Consulta por perfil: Cliente tem {len(apps_cli)} e Prestador tem {len(apps_prest)} agendamentos.")
    print("    [PASS] Teste 4 APROVADO: Isolamento e consulta por perfil validados.")

    # 6. Teste de atualização de status (Conclusão)
    suc_up, app_up = appointment_service.update_appointment_status(app_id, "concluido")
    assert suc_up is True and app_up.get("status") == "concluido", "Falha ao concluir agendamento!"
    print("    [PASS] Teste 5 APROVADO: Conclusão de atendimento atualizada com sucesso.")

    # 7. Teste de cancelamento e liberação do slot
    # Cria novo agendamento no próximo slot
    slots_restantes = appointment_service.calculate_available_slots(prestador_id, data_teste, 30)
    slot_teste_cancel = slots_restantes[1]
    suc_c, app_c = appointment_service.create_appointment(cliente_id, prestador_id, 1, data_teste, slot_teste_cancel)
    assert suc_c is True
    
    # Verifica que o slot sumiu
    slots_pos_reserva = appointment_service.calculate_available_slots(prestador_id, data_teste, 30)
    assert slot_teste_cancel not in slots_pos_reserva, "Slot deveria estar ocupado!"

    # Cancela o agendamento
    appointment_service.update_appointment_status(app_c["id"], "cancelado")
    
    # Verifica que o slot voltou a ficar livre
    slots_pos_cancel = appointment_service.calculate_available_slots(prestador_id, data_teste, 30)
    assert slot_teste_cancel in slots_pos_cancel, "Slot cancelado deveria voltar a ficar disponível!"
    print("    [PASS] Teste 6 APROVADO: Cancelamento libera o horário imediatamente.")

    print("\n==================================================")
    print("[SUCCESS] TODOS OS TESTES DO MOTOR DE AGENDAMENTOS PASSARAM COM SUCESSO!")
    print("==================================================")


if __name__ == "__main__":
    try:
        run_tests()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] FALHA NO TESTE: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] ERRO INESPERADO: {e}")
        sys.exit(1)
