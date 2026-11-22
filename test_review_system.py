"""
Testes automatizados completos para o Sistema de Avaliações e Reputação (AgendAí) - Fase 0.
Valida:
1. Nota 1 (obrigatória e aceita normalmente).
2. Nota 5 (obrigatória e aceita normalmente).
3. Nota ausente ou inválida (bloqueada com mensagem descritiva).
4. Avaliação duplicada (bloqueada no mesmo agendamento).
5. Atendimento não concluído (bloqueado).
6. Cliente diferente do titular (bloqueado).
7. IDs com tipos divergentes (int x str) e status acentuado ("concluído").
8. Erro do Xano na gravação (resiliência ativa sem perder o dado).
9. Formatação segura de nome e métricas contextuais por serviço.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from services import review_service, appointment_service, ui_utils


def test_nota_1():
    """Valida que a nota 1 é aceita normalmente como avaliação válida."""
    val, msg = review_service.validate_review_input(1, "Atendimento regular")
    assert val is True
    assert msg == ""


def test_nota_5():
    """Valida que a nota 5 é aceita normalmente."""
    val, msg = review_service.validate_review_input(5, "Serviço perfeito!")
    assert val is True
    assert msg == ""


def test_nota_ausente_ou_invalida():
    """Valida que notas fora do intervalo 1-5, ausentes ou nulas falham."""
    for n in (None, "", "abc", 0, 6, -1):
        val, msg = review_service.validate_review_input(n, "Comentário")
        assert val is False
        assert len(msg) > 0


def test_review_duplicada_bloqueada():
    """Valida que um atendimento não pode ser avaliado mais de uma vez."""
    import time
    app_id = int(time.time() * 1000) % 1000000 + 10000
    appointment_service.MOCK_APPOINTMENTS.append({
        "id": app_id,
        "cliente_id": "15",
        "prestador_id": "1",
        "servico_id": "1",
        "status": "concluido"
    })
    
    # Primeira submissão
    suc1, resp1 = review_service.submit_review(
        agendamento_id=app_id,
        cliente_id="15",
        prestador_id="1",
        nota=5,
        comentario="Primeira avaliação",
        cliente_nome="Hector Barros"
    )
    assert suc1 is True, f"Falha na primeira submissão: {resp1}"

    # Segunda submissão (deve ser bloqueada)
    suc2, resp2 = review_service.submit_review(
        agendamento_id=app_id,
        cliente_id="15",
        prestador_id="1",
        nota=4,
        comentario="Tentativa duplicada",
        cliente_nome="Hector Barros"
    )
    assert suc2 is False
    assert "já foi avaliado" in resp2.get("message", "")


def test_atendimento_nao_concluido_bloqueado():
    """Valida que agendamentos pendentes ou confirmados não podem ser avaliados."""
    for status_invalido in ("pendente", "confirmado", "cancelado"):
        app_id = f"test_st_{status_invalido}"
        appointment_service.MOCK_APPOINTMENTS.append({
            "id": app_id,
            "cliente_id": "15",
            "prestador_id": "1",
            "servico_id": "1",
            "status": status_invalido
        })
        suc, resp = review_service.submit_review(
            agendamento_id=app_id,
            cliente_id="15",
            prestador_id="1",
            nota=5,
            comentario="Não concluído",
            cliente_nome="Hector Barros"
        )
        assert suc is False
        assert "Apenas atendimentos marcados como concluídos" in resp.get("message", "")


def test_cliente_diferente_bloqueado():
    """Valida que apenas o titular do agendamento pode avaliá-lo."""
    app_id = 9982
    appointment_service.MOCK_APPOINTMENTS.append({
        "id": app_id,
        "cliente_id": "15",
        "prestador_id": "1",
        "servico_id": "1",
        "status": "concluido"
    })
    # Tentativa com cliente_id diferente
    suc, resp = review_service.submit_review(
        agendamento_id=app_id,
        cliente_id="99",
        prestador_id="1",
        nota=5,
        comentario="Intruso",
        cliente_nome="Outro Cliente"
    )
    assert suc is False
    assert "Apenas o cliente titular" in resp.get("message", "")


def test_tipos_divergentes_int_str_e_status_acento():
    """
    Valida a normalização de tipos (int x str) e status acentuado ('concluído').
    Cenário que reproduziu o bug no fluxo real do Hector.
    """
    import time
    app_id = int(time.time() * 1000) % 1000000 + 30000
    appointment_service.MOCK_APPOINTMENTS.append({
        "id": str(app_id),
        "cliente_id": "15",  # string
        "prestador_id": 1,
        "servico_id": 1,
        "status": "Concluído"  # acentuado e com maiúscula
    })

    # Submissão passando cliente_id como int 15 e agendamento_id como int
    suc, resp = review_service.submit_review(
        agendamento_id=app_id,
        cliente_id=15,  # int
        prestador_id=1,
        nota=1,
        comentario="Nota 1 funciona com sucesso!",
        cliente_nome="Hector Barros",
        servico_id=1
    )
    assert suc is True, f"Falha na avaliação com tipos mistos e acento: {resp}"
    assert review_service.is_appointment_reviewed(app_id) is True
    assert review_service.is_appointment_reviewed(str(app_id)) is True


def test_erro_xano_resiliencia_e_nao_perda_do_dado():
    """
    Valida que, caso o Xano retorne erro ou falhe conexão, a avaliação é
    gravada no fallback local de forma resiliente, sem perda nem duplicidade.
    """
    import time
    app_id = int(time.time() * 1000) % 1000000 + 40000
    appointment_service.MOCK_APPOINTMENTS.append({
        "id": app_id,
        "cliente_id": "2",
        "prestador_id": "15",
        "servico_id": "1",
        "servico_titulo": "Corte Especial",
        "status": "concluido"
    })

    # Token fictício que forçará mock se a conexão falhar
    suc, resp = review_service.submit_review(
        agendamento_id=app_id,
        cliente_id="2",
        prestador_id="15",
        nota=5,
        comentario="Avaliação resiliente",
        cliente_nome="Mariana Silva",
        servico_id="1",
        token="invalid_token_test"
    )
    assert suc is True
    assert resp.get("agendamento_id") == str(app_id)
    assert resp.get("nota") == 5

    # Confirma que a avaliação está acessível em get_reviews
    _, revs = review_service.get_reviews(servico_id="1")
    encontrado = any(str(r.get("agendamento_id")) == str(app_id) for r in revs)
    assert encontrado is True, "Avaliação não encontrada na listagem local após fallback do Xano."


def test_format_client_name():
    assert review_service.format_client_name("Lucas Ferreira") == "Lucas F."
    assert review_service.format_client_name("Mariana Silva Santos") == "Mariana S."
    assert review_service.format_client_name("Carlos") == "Carlos"
    assert review_service.format_client_name("") == "Cliente"
    assert review_service.format_client_name(None) == "Cliente"


def test_persistencia_disco_e_bloqueio_apos_restart():
    """Valida que avaliações e agendamentos avaliados persistem no disco e são reconhecidos após restart do módulo."""
    import importlib
    import time
    app_id = int(time.time() * 1000) % 1000000 + 20000
    appointment_service.MOCK_APPOINTMENTS.append({
        "id": app_id,
        "cliente_id": "77",
        "prestador_id": "15",
        "servico_id": "2",
        "status": "concluido"
    })

    # Submete avaliação
    suc, resp = review_service.submit_review(
        agendamento_id=app_id,
        cliente_id="77",
        prestador_id="15",
        nota=4,
        comentario="Serviço excelente e persistente",
        cliente_nome="Fernando Souza",
        servico_id="2",
        token="token_simulado"
    )
    assert suc is True

    # Verifica se gravou no arquivo reviewed_appointments.json
    rev_apps = review_service._load_reviewed_appointments()
    assert str(app_id) in rev_apps

    # Simula restart completo do módulo review_service recarregando do disco
    importlib.reload(review_service)

    # 1. Verifica se is_appointment_reviewed reconhece mesmo após o reload
    assert review_service.is_appointment_reviewed(app_id) is True

    # 2. Verifica se a avaliação aparece em get_reviews
    _, revs = review_service.get_reviews(servico_id="2")
    encontrado = any(str(r.get("agendamento_id")) == str(app_id) for r in revs)
    assert encontrado is True, "Avaliação persistida não encontrada após recarga do módulo."

    # 3. Verifica se as métricas foram atualizadas
    metrics = review_service.get_metrics(servico_id="2")
    assert metrics.get("total_avaliacoes", 0) >= 1
    assert metrics.get("nota_media", 0) > 0


def run_all():
    print("Executando test_nota_1...")
    test_nota_1()
    print("Executando test_nota_5...")
    test_nota_5()
    print("Executando test_nota_ausente_ou_invalida...")
    test_nota_ausente_ou_invalida()
    print("Executando test_review_duplicada_bloqueada...")
    test_review_duplicada_bloqueada()
    print("Executando test_atendimento_nao_concluido_bloqueado...")
    test_atendimento_nao_concluido_bloqueado()
    print("Executando test_cliente_diferente_bloqueado...")
    test_cliente_diferente_bloqueado()
    print("Executando test_tipos_divergentes_int_str_e_status_acento...")
    test_tipos_divergentes_int_str_e_status_acento()
    print("Executando test_erro_xano_resiliencia_e_nao_perda_do_dado...")
    test_erro_xano_resiliencia_e_nao_perda_do_dado()
    print("Executando test_format_client_name...")
    test_format_client_name()
    print("Executando test_persistencia_disco_e_bloqueio_apos_restart...")
    test_persistencia_disco_e_bloqueio_apos_restart()
    print("\n[SUCESSO] Todos os testes do sistema de avaliações passaram com 100% de conformidade!")


if __name__ == "__main__":
    run_all()
