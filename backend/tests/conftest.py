"""
Configuração dos testes: usa um banco SQLite em memória, então não precisa
de PostgreSQL nem de arquivo .env para rodar (nem localmente, nem no CI).
"""
import pytest

from app import create_app
from app.config import Config
from app.extensions import db
from app.models import Usuario


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "chave-de-teste-com-tamanho-suficiente-123456"
    SECRET_KEY = "chave-de-teste"


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        for nome, email, perfil, senha in [
            ("Admin", "admin@teste.com", "admin", "admin123"),
            ("Professor", "prof@teste.com", "professor", "prof123"),
        ]:
            u = Usuario(nome=nome, email=email, perfil=perfil)
            u.set_senha(senha)
            db.session.add(u)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def fazer_login(client, email, senha):
    return client.post("/api/auth/login", json={"email": email, "senha": senha})


@pytest.fixture()
def token_admin(client):
    return fazer_login(client, "admin@teste.com", "admin123").get_json()["dados"]["token"]


@pytest.fixture()
def token_professor(client):
    return fazer_login(client, "prof@teste.com", "prof123").get_json()["dados"]["token"]
