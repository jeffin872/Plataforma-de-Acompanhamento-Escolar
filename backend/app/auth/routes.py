from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt

from app.extensions import db
from app.models import Usuario
from app.utils.responses import sucesso, erro
from app.auth.decorators import perfil_requerido, usuario_logado_id

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    """
    Autentica o usuário e devolve um token JWT contendo o `perfil` como
    claim extra. É esse claim que os decorators usam para bloquear acesso
    indevido entre Administrador, Professor e Responsável.
    """
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    senha = payload.get("senha") or ""

    if not email or not senha:
        return erro("Informe e-mail e senha.", status=400)

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.checar_senha(senha):
        return erro("E-mail ou senha inválidos.", status=401)

    if not usuario.ativo:
        return erro("Este usuário está desativado. Procure a administração da escola.", status=403)

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={"perfil": usuario.perfil, "nome": usuario.nome},
    )
    return sucesso(
        dados={"token": token, "usuario": usuario.to_dict()},
        mensagem="Login realizado com sucesso.",
    )


@auth_bp.get("/me")
@perfil_requerido("admin", "professor", "responsavel")
def meus_dados():
    usuario = Usuario.query.get(usuario_logado_id())
    if not usuario:
        return erro("Usuário não encontrado.", status=404)
    return sucesso(dados=usuario.to_dict())


@auth_bp.put("/senha")
@perfil_requerido("admin", "professor", "responsavel")
def trocar_senha():
    payload = request.get_json(silent=True) or {}
    senha_atual = payload.get("senha_atual") or ""
    nova_senha = payload.get("nova_senha") or ""

    usuario = Usuario.query.get(usuario_logado_id())
    if not usuario or not usuario.checar_senha(senha_atual):
        return erro("Senha atual incorreta.", status=401)

    if len(nova_senha) < 6:
        return erro("A nova senha deve ter pelo menos 6 caracteres.", status=400)

    usuario.set_senha(nova_senha)
    db.session.commit()
    return sucesso(mensagem="Senha alterada com sucesso.")
