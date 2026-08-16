from datetime import datetime, date

from flask import Blueprint, request

from app.extensions import db
from app.models import (
    Aluno, Nota, Falta, Ocorrencia, TurmaDisciplinaProfessor,
)
from app.models.ocorrencia import TIPOS_OCORRENCIA
from app.utils.responses import sucesso, erro
from app.auth.decorators import perfil_requerido, usuario_logado_id
from app.academic.helpers import professor_pode_lecionar, aluno_pertence_a_turma
from app.alerts.service import verificar_excesso_faltas

academic_bp = Blueprint("academic", __name__, url_prefix="/api/academic")


def _parse_data(valor_str, campo="data"):
    if not valor_str:
        return date.today()
    try:
        return datetime.strptime(valor_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Campo '{campo}' inválido. Use o formato AAAA-MM-DD.")


@academic_bp.get("/minhas-turmas")
@perfil_requerido("professor")
def minhas_turmas():
    """Lista as turmas + disciplinas que o professor logado está autorizado a lecionar."""
    vinculos = TurmaDisciplinaProfessor.query.filter_by(
        professor_id=usuario_logado_id()
    ).all()
    return sucesso(dados=[v.to_dict() for v in vinculos])


# ---------------------------------------------------------------------------
# Notas
# ---------------------------------------------------------------------------

@academic_bp.post("/notas")
@perfil_requerido("professor")
def lancar_nota():
    professor_id = usuario_logado_id()
    payload = request.get_json(silent=True) or {}

    aluno_id = payload.get("aluno_id")
    turma_id = payload.get("turma_id")
    disciplina_id = payload.get("disciplina_id")

    aluno = Aluno.query.get(aluno_id)
    if not aluno_pertence_a_turma(aluno, turma_id):
        return erro("O aluno não pertence a esta turma.", status=400)
    if not professor_pode_lecionar(professor_id, turma_id, disciplina_id):
        return erro("Você não está vinculado a esta disciplina nesta turma.", status=403)

    try:
        valor = Nota.validar_valor(payload.get("valor"))
        data_avaliacao = _parse_data(payload.get("data_avaliacao"), "data_avaliacao")
    except (ValueError, TypeError) as exc:
        return erro(str(exc), status=400)

    nota = Nota(
        aluno_id=aluno_id, turma_id=turma_id, disciplina_id=disciplina_id,
        professor_id=professor_id, valor=valor, etapa=payload.get("etapa"),
        data_avaliacao=data_avaliacao,
    )
    db.session.add(nota)
    db.session.commit()
    return sucesso(dados=nota.to_dict(), mensagem="Nota lançada com sucesso.", status=201)


@academic_bp.get("/turmas/<int:turma_id>/notas")
@perfil_requerido("professor", "admin")
def listar_notas_da_turma(turma_id):
    notas = Nota.query.filter_by(turma_id=turma_id).order_by(Nota.data_avaliacao.desc()).all()
    return sucesso(dados=[n.to_dict() for n in notas])


# ---------------------------------------------------------------------------
# Faltas
# ---------------------------------------------------------------------------

@academic_bp.post("/faltas")
@perfil_requerido("professor")
def registrar_falta():
    payload = request.get_json(silent=True) or {}
    aluno_id = payload.get("aluno_id")
    turma_id = payload.get("turma_id")

    aluno = Aluno.query.get(aluno_id)
    if not aluno_pertence_a_turma(aluno, turma_id):
        return erro("O aluno não pertence a esta turma.", status=400)

    try:
        data_falta = _parse_data(payload.get("data_falta"), "data_falta")
    except ValueError as exc:
        return erro(str(exc), status=400)

    falta = Falta(aluno_id=aluno_id, turma_id=turma_id, data_falta=data_falta)
    db.session.add(falta)
    db.session.commit()

    # Módulo de Alertas: verifica se esse aluno passou do limite de faltas
    # não justificadas e, se sim, dispara e-mail + notificação automática.
    verificar_excesso_faltas(aluno_id)

    return sucesso(dados=falta.to_dict(), mensagem="Falta registrada com sucesso.", status=201)


@academic_bp.put("/faltas/<int:falta_id>/justificar")
@perfil_requerido("professor", "admin")
def justificar_falta(falta_id):
    falta = Falta.query.get(falta_id)
    if not falta:
        return erro("Falta não encontrada.", status=404)

    payload = request.get_json(silent=True) or {}
    try:
        falta.justificar(payload.get("motivo"))
    except ValueError as exc:
        return erro(str(exc), status=400)

    db.session.commit()
    return sucesso(dados=falta.to_dict(), mensagem="Falta justificada com sucesso.")


@academic_bp.get("/turmas/<int:turma_id>/faltas")
@perfil_requerido("professor", "admin")
def listar_faltas_da_turma(turma_id):
    faltas = Falta.query.filter_by(turma_id=turma_id).order_by(Falta.data_falta.desc()).all()
    return sucesso(dados=[f.to_dict() for f in faltas])


# ---------------------------------------------------------------------------
# Ocorrências
# ---------------------------------------------------------------------------

@academic_bp.post("/ocorrencias")
@perfil_requerido("professor")
def registrar_ocorrencia():
    professor_id = usuario_logado_id()
    payload = request.get_json(silent=True) or {}

    aluno_id = payload.get("aluno_id")
    turma_id = payload.get("turma_id")
    tipo = payload.get("tipo")
    descricao = (payload.get("descricao") or "").strip()

    aluno = Aluno.query.get(aluno_id)
    if not aluno_pertence_a_turma(aluno, turma_id):
        return erro("O aluno não pertence a esta turma.", status=400)
    if tipo not in TIPOS_OCORRENCIA:
        return erro(f"Tipo inválido. Use um de: {', '.join(TIPOS_OCORRENCIA)}.", status=400)
    if not descricao:
        return erro("Descreva a ocorrência.", status=400)

    try:
        data_ocorrencia = _parse_data(payload.get("data_ocorrencia"), "data_ocorrencia")
    except ValueError as exc:
        return erro(str(exc), status=400)

    ocorrencia = Ocorrencia(
        aluno_id=aluno_id, turma_id=turma_id, professor_id=professor_id,
        tipo=tipo, descricao=descricao, data_ocorrencia=data_ocorrencia,
    )
    db.session.add(ocorrencia)
    db.session.commit()
    return sucesso(
        dados=ocorrencia.to_dict(), mensagem="Ocorrência registrada com sucesso.", status=201
    )


@academic_bp.get("/turmas/<int:turma_id>/ocorrencias")
@perfil_requerido("professor", "admin")
def listar_ocorrencias_da_turma(turma_id):
    ocorrencias = (
        Ocorrencia.query.filter_by(turma_id=turma_id)
        .order_by(Ocorrencia.data_ocorrencia.desc())
        .all()
    )
    return sucesso(dados=[o.to_dict() for o in ocorrencias])
