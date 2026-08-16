"""
Decorators que aplicam a regra "Separação por Perfil": cada rota da API
declara quais perfis podem acessá-la, e qualquer outro perfil recebe 403.
"""
from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

from app.utils.responses import erro


def perfil_requerido(*perfis_permitidos):
    """
    Uso:
        @perfil_requerido("admin")
        @perfil_requerido("admin", "professor")
    """
    def decorador(funcao_rota):
        @wraps(funcao_rota)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            perfil_atual = claims.get("perfil")
            if perfil_atual not in perfis_permitidos:
                return erro(
                    "Você não tem permissão para acessar este recurso.", status=403
                )
            return funcao_rota(*args, **kwargs)
        return wrapper
    return decorador


def usuario_logado_id() -> int:
    """Atalho para pegar o id do usuário autenticado dentro de uma rota."""
    return int(get_jwt_identity())
