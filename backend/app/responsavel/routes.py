from flask import Blueprint

from app.models import Aluno, ResponsavelAluno, Nota, Falta, Ocorrencia, Notificacao
from app.utils.responses import sucesso, erro
from app.auth.decorators import perfil_requerido, usuario_logado_id

responsavel_bp = Blueprint("responsavel", __name__, url_prefix="/api/responsavel")


def _aluno_do_responsavel_ou_none(aluno_id: int, responsavel_id: int):
    """
    Trava de segurança central deste módulo: um responsável só pode ver
    dados de alunos formalmente vinculados a ele (tabela ResponsavelAluno).
    """
    vinculo = ResponsavelAluno.query.filter_by(
        responsavel_id=responsavel_id, aluno_id=aluno_id
    ).first()
    if not vinculo:
        return None
    return Aluno.query.get(aluno_id)


@responsavel_bp.get("/meus-alunos")
@perfil_requerido("responsavel")
def meus_alunos():
    responsavel_id = usuario_logado_id()
    vinculos = ResponsavelAluno.query.filter_by(responsavel_id=responsavel_id).all()
    alunos = [v.aluno.to_dict() for v in vinculos]
    return sucesso(dados=alunos)


@responsavel_bp.get("/alunos/<int:aluno_id>/notas")
@perfil_requerido("responsavel")
def notas_do_aluno(aluno_id):
    aluno = _aluno_do_responsavel_ou_none(aluno_id, usuario_logado_id())
    if not aluno:
        return erro("Aluno não encontrado ou não vinculado a você.", status=404)
    notas = Nota.query.filter_by(aluno_id=aluno_id).order_by(Nota.data_avaliacao.desc()).all()
    return sucesso(dados=[n.to_dict() for n in notas])


@responsavel_bp.get("/alunos/<int:aluno_id>/faltas")
@perfil_requerido("responsavel")
def faltas_do_aluno(aluno_id):
    aluno = _aluno_do_responsavel_ou_none(aluno_id, usuario_logado_id())
    if not aluno:
        return erro("Aluno não encontrado ou não vinculado a você.", status=404)
    faltas = Falta.query.filter_by(aluno_id=aluno_id).order_by(Falta.data_falta.desc()).all()
    return sucesso(dados={
        "faltas": [f.to_dict() for f in faltas],
        "total": len(faltas),
        "nao_justificadas": len([f for f in faltas if not f.justificada]),
    })


@responsavel_bp.get("/alunos/<int:aluno_id>/ocorrencias")
@perfil_requerido("responsavel")
def ocorrencias_do_aluno(aluno_id):
    aluno = _aluno_do_responsavel_ou_none(aluno_id, usuario_logado_id())
    if not aluno:
        return erro("Aluno não encontrado ou não vinculado a você.", status=404)
    ocorrencias = (
        Ocorrencia.query.filter_by(aluno_id=aluno_id)
        .order_by(Ocorrencia.data_ocorrencia.desc())
        .all()
    )
    return sucesso(dados=[o.to_dict() for o in ocorrencias])


@responsavel_bp.get("/notificacoes")
@perfil_requerido("responsavel")
def minhas_notificacoes():
    notificacoes = (
        Notificacao.query.filter_by(usuario_id=usuario_logado_id())
        .order_by(Notificacao.criado_em.desc())
        .all()
    )
    return sucesso(dados=[n.to_dict() for n in notificacoes])
