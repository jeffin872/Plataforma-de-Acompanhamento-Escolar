from app.models import Usuario


def test_senha_e_guardada_como_hash():
    u = Usuario(nome="Teste", email="t@t.com", perfil="admin")
    u.set_senha("minha-senha")
    assert u.senha_hash != "minha-senha"
    assert u.checar_senha("minha-senha") is True
    assert u.checar_senha("outra") is False
