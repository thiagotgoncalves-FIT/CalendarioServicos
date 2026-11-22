"""
Suíte de testes unitários para a funcionalidade de Configurações da Conta:
- Validação e máscara de telefone brasileiro
- Atualização cadastral de perfil (nome e telefone)
- Validação e alteração segura de senha
- Upload, validação de formato/tamanho e remoção de foto de perfil (avatar)
- Persistência e injeção dinâmica de temas (Claro e Escuro)
"""

import os
import sys
import json
from pathlib import Path

# Adiciona diretório raiz ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from services import auth_service, ui_utils


def test_phone_validation_and_masking():
    print("Executando test_phone_validation_and_masking...")
    # Celular com 11 dígitos
    val, fmt, clean = auth_service.validate_phone_br("11987654321")
    assert val is True
    assert fmt == "(11) 98765-4321"
    assert clean == "11987654321"

    # Fixo com 10 dígitos
    val, fmt, clean = auth_service.validate_phone_br("1133334444")
    assert val is True
    assert fmt == "(11) 3333-4444"
    assert clean == "1133334444"

    # Telefone já com pontuação/espaços
    val, fmt, clean = auth_service.validate_phone_br(" (11) 98888-7777 ")
    assert val is True
    assert fmt == "(11) 98888-7777"
    assert clean == "11988887777"

    # Inválido: menos de 10 dígitos
    val, fmt, msg = auth_service.validate_phone_br("12345")
    assert val is False
    assert "válido com DDD" in msg

    # Inválido: DDD inexistente (menor que 11)
    val, fmt, msg = auth_service.validate_phone_br("05988887777")
    assert val is False
    assert "DDD inválido" in msg

    print("  ✓ Validação e máscara de telefone aprovadas.")


def test_update_user_profile():
    print("Executando test_update_user_profile...")
    user_id = 1  # Carlos Barbeiro
    email = "carlos@barbearia.com"

    # Sucesso com persistência
    suc, res = auth_service.update_user_profile(user_id, "Carlos Augusto Barbeiro", "11988889999", email=email)
    assert suc is True
    assert res["user"]["name"] == "Carlos Augusto Barbeiro"
    assert res["user"]["phone"] == "11988889999"

    # Valida gravação no arquivo persistente uploads/user_profiles.json
    persisted_profiles = auth_service._load_persisted_profiles()
    assert email in persisted_profiles
    assert persisted_profiles[email]["name"] == "Carlos Augusto Barbeiro"
    assert persisted_profiles[email]["phone"] == "11988889999"

    # Validação de nome muito curto
    suc, res = auth_service.update_user_profile(user_id, "A", "11988889999", email=email)
    assert suc is False
    assert "pelo menos 2 caracteres" in res["message"]

    # Validação de telefone inválido
    suc, res = auth_service.update_user_profile(user_id, "Carlos", "abc", email=email)
    assert suc is False

    # Valida login subsequente carregando os dados do arquivo persistente
    suc_log, res_log = auth_service.login(email, "123")
    if suc_log:
        assert res_log["user"]["name"] == "Carlos Augusto Barbeiro"
        assert res_log["user"]["phone"] == "11988889999"

    print("  ✓ Atualização de perfil cadastral e persistência em disco aprovadas.")


def test_password_change_flow():
    print("Executando test_password_change_flow...")
    user_id = 2  # Mariana Silva
    # Restaura senha inicial no mock e arquivo para teste limpo
    auth_service._MOCK_USERS_DB["mariana@email.com"]["password"] = "123"
    persisted = auth_service._load_persisted_credentials()
    if "mariana@email.com" in persisted:
        del persisted["mariana@email.com"]
        with open(auth_service.CREDENTIALS_FILE, "w", encoding="utf-8") as f:
            json.dump(persisted, f)

    # Falha: senha atual incorreta
    suc, res = auth_service.change_password(user_id, "senha_errada", "NovaSenha123", "NovaSenha123")
    assert suc is False
    assert "incorreta" in res["message"]

    # Falha: nova senha muito curta (< 8 chars)
    suc, res = auth_service.change_password(user_id, "123", "abc1", "abc1")
    assert suc is False
    assert "mínimo 8 caracteres" in res["message"]

    # Falha: nova senha sem números
    suc, res = auth_service.change_password(user_id, "123", "senhaapenasletras", "senhaapenasletras")
    assert suc is False
    assert "letra e um número" in res["message"]

    # Falha: divergência na confirmação
    suc, res = auth_service.change_password(user_id, "123", "NovaSenha123", "OutraCoisa123")
    assert suc is False
    assert "confirmação" in res["message"]

    # Sucesso: alteração com senha atual válida
    suc, res = auth_service.change_password(user_id, "123", "NovaSenha123", "NovaSenha123")
    assert suc is True
    assert "sucesso" in res["message"]

    # Verifica que a senha foi atualizada e agora a anterior não funciona mais
    suc_antiga, _ = auth_service.change_password(user_id, "123", "OutraSenha456", "OutraSenha456")
    assert suc_antiga is False

    print("  ✓ Fluxo de alteração de senha e regras de força aprovados.")


def test_avatar_upload_and_removal():
    print("Executando test_avatar_upload_and_removal...")
    user_id = 15  # Hector Barros
    mock_png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 1024  # 1 KB

    # Rejeição de formato não permitido (.pdf)
    suc, res = auth_service.save_user_avatar(user_id, mock_png_bytes, "documento.pdf")
    assert suc is False
    assert "Formato de arquivo inválido" in res["message"]

    # Rejeição de arquivo > 2 MB
    too_large_bytes = b"\x00" * (2 * 1024 * 1024 + 10)
    suc, res = auth_service.save_user_avatar(user_id, too_large_bytes, "foto.png")
    assert suc is False
    assert "excede o tamanho máximo" in res["message"]

    # Sucesso: upload de imagem válida PNG
    suc, res = auth_service.save_user_avatar(user_id, mock_png_bytes, "minha_foto.png")
    assert suc is True
    saved_path = res["photo_url"]
    assert os.path.exists(saved_path)

    # Teste de persistência e reconciliação automática no login
    suc_log, res_log = auth_service.login("hector.barros@aluno.impacta.edu.br", "123")
    assert suc_log is True
    logged_user = res_log["user"]
    assert logged_user.get("photo_url") is not None
    assert os.path.exists(logged_user["photo_url"])

    # Renderização HTML do avatar com foto
    fake_user = {"name": "Hector Barros", "photo_url": saved_path}
    avatar_html = ui_utils.user_avatar_html(fake_user, size=60)
    assert "<img" in avatar_html
    assert "data:image/png;base64," in avatar_html
    assert "border-radius:50%" in avatar_html

    # Remoção da foto
    suc_rem, res_rem = auth_service.remove_user_avatar(user_id)
    assert suc_rem is True
    assert not os.path.exists(saved_path)

    # Renderização HTML após remoção (fallback para iniciais)
    fake_user_sem_foto = {"name": "Hector Barros", "photo_url": None}
    avatar_iniciais = ui_utils.user_avatar_html(fake_user_sem_foto, size=60)
    assert "HB" in avatar_iniciais
    assert "<img" not in avatar_iniciais

    print("  ✓ Upload, validação e remoção de avatar aprovados.")


def test_theme_persistence_and_styles():
    print("Executando test_theme_persistence_and_styles...")
    user_id = 15

    # Atualiza para tema escuro
    suc, res = auth_service.update_user_theme(user_id, "escuro")
    assert suc is True
    assert res["theme"] == "escuro"

    # Atualiza para tema claro
    suc, res = auth_service.update_user_theme(user_id, "claro")
    assert suc is True
    assert res["theme"] == "claro"

    # Rejeita tema desconhecido
    suc, res = auth_service.update_user_theme(user_id, "neon")
    assert suc is False
    assert "Tema inválido" in res["message"]

    # Valida CSS dinâmico gerado para Tema Escuro
    dark_css = ui_utils.apply_theme_and_clean_ui("escuro")
    assert "#0B0F19" in dark_css
    assert "header[data-testid=\"stHeader\"]" in dark_css
    assert "display: none !important" in dark_css

    # Valida CSS dinâmico gerado para Tema Claro
    light_css = ui_utils.apply_theme_and_clean_ui("claro")
    assert "#F8FAFC" in light_css
    assert "header[data-testid=\"stHeader\"]" in light_css

    print("  ✓ Persistência e injeção de estilos de temas aprovados.")


if __name__ == "__main__":
    print("\n==================================================")
    print("[TEST] INICIANDO TESTES DE CONFIGURAÇÕES DA CONTA")
    print("==================================================")
    test_phone_validation_and_masking()
    test_update_user_profile()
    test_password_change_flow()
    test_avatar_upload_and_removal()
    test_theme_persistence_and_styles()
    print("\n[SUCESSO] Todos os testes de configurações da conta passaram com 100% de conformidade!")
    print("==================================================\n")

