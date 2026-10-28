from tests.conftest import fazer_login


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_saude_retorna_ok(client):
    resp = client.get("/api/saude")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_rota_inexistente_retorna_404_padronizado(client):
    resp = client.get("/api/nao-existe")
    assert resp.status_code == 404
    assert resp.get_json()["sucesso"] is False


def test_login_com_credenciais_validas(client):
    resp = fazer_login(client, "admin@teste.com", "admin123")
    assert resp.status_code == 200
    assert "token" in resp.get_json()["dados"]


def test_login_com_senha_errada(client):
    resp = fazer_login(client, "admin@teste.com", "senha-errada")
    assert resp.status_code == 401


def test_login_sem_campos_retorna_400(client):
    resp = client.post("/api/auth/login", json={})
    assert resp.status_code == 400


def test_rota_protegida_sem_token_retorna_401(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_me_com_token_retorna_usuario(client, token_admin):
    resp = client.get("/api/auth/me", headers=auth(token_admin))
    assert resp.status_code == 200
    assert resp.get_json()["dados"]["email"] == "admin@teste.com"


def test_admin_acessa_rota_de_admin(client, token_admin):
    resp = client.get("/api/admin/usuarios", headers=auth(token_admin))
    assert resp.status_code == 200


def test_professor_nao_acessa_rota_de_admin(client, token_professor):
    """Separação por perfil: professor deve receber 403 em rota de admin."""
    resp = client.get("/api/admin/usuarios", headers=auth(token_professor))
    assert resp.status_code == 403
