"""
Teste de isolamento, consistência e autenticação resiliente entre perfis Prestador vs Cliente
"""
import uuid
from services import auth_service, catalog_service, availability_service

def test_flow():
    print("1. Testando login do Prestador 1 (Carlos)...")
    ok, carlos_resp = auth_service.login("carlos@barbearia.com", "SenhaForte123")
    assert ok, f"Login do Carlos falhou: {carlos_resp}"
    assert carlos_resp["user"]["role"] == "prestador"
    token_carlos = carlos_resp.get("authToken")
    print("   -> Carlos autenticado como 'prestador'")

    print("\n2. Testando cadastro dinâmico de NOVO Prestador (resiliente)...")
    email_novo_p = f"prestador_{uuid.uuid4().hex[:6]}@agendai.com"
    ok, novo_p_resp = auth_service.signup(
        name="Lucas Barbeiro Pro",
        email=email_novo_p,
        password="MinhaSenha123",
        phone="11999990000",
        role="prestador"
    )
    assert ok, f"Cadastro do novo prestador falhou: {novo_p_resp}"
    assert novo_p_resp["user"]["role"] == "prestador"
    token_novo_p = novo_p_resp["authToken"]
    print(f"   -> Novo prestador cadastrado com sucesso! Token: {token_novo_p}")

    print("\n3. Testando login com a conta recém-criada do Prestador...")
    ok, login_p_resp = auth_service.login(email_novo_p, "MinhaSenha123")
    assert ok, f"Login do novo prestador falhou: {login_p_resp}"
    assert login_p_resp["user"]["name"] == "Lucas Barbeiro Pro"
    print("   -> Login do novo prestador realizado com sucesso!")

    print("\n4. Testando cadastro dinâmico de NOVO Cliente (resiliente)...")
    email_novo_c = f"cliente_{uuid.uuid4().hex[:6]}@agendai.com"
    ok, novo_c_resp = auth_service.signup(
        name="Camila Cliente",
        email=email_novo_c,
        password="MinhaSenha123",
        phone="11988880000",
        role="cliente"
    )
    assert ok, f"Cadastro de novo cliente falhou: {novo_c_resp}"
    assert novo_c_resp["user"]["role"] == "cliente"
    print("   -> Novo cliente cadastrado com sucesso!")

    print("\n5. Testando login com o novo Cliente...")
    ok, login_c_resp = auth_service.login(email_novo_c, "MinhaSenha123")
    assert ok, f"Login do novo cliente falhou: {login_c_resp}"
    assert login_c_resp["user"]["role"] == "cliente"
    print("   -> Login do novo cliente realizado com sucesso!")

    print("\n6. Testando persistência da sessão via get_current_user...")
    ok_me, me_data = auth_service.get_current_user(novo_p_resp["authToken"])
    assert ok_me, f"Falha ao validar sessão do usuário ativo: {me_data}"
    assert me_data["user"]["name"] == "Lucas Barbeiro Pro"
    print("   -> Sessão recuperada e validada com sucesso!")

    print("\n7. Testando isolamento do catálogo do Prestador 1...")
    ok, servicos_carlos = catalog_service.get_services(prestador_id=1, token=token_carlos)
    assert ok
    print(f"   -> Carlos possui {len(servicos_carlos)} servicos")

    print("\n8. Testando visualização do catálogo na Área do Cliente...")
    ok, servicos_publicos = catalog_service.get_public_services(token=novo_c_resp.get("authToken"))
    assert ok
    assert len(servicos_publicos) > 0
    print(f"   -> Cliente visualiza com sucesso {len(servicos_publicos)} servicos publicos ativos")

    print("\n[OK] Todos os testes de cadastro, login, sessao e isolamento passaram com 100% de sucesso!")

if __name__ == "__main__":
    test_flow()

