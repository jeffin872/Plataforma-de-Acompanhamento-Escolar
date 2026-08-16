from datetime import datetime

from flask import Blueprint, request

from app.extensions import db
from app.models import (
    Usuario, Turma, Disciplina, TurmaDisciplinaProfessor,
    Aluno, ResponsavelAluno, Nota, Falta, Documento,
)
from app.models.usuario import PERFIS_VALIDOS
from app.utils.responses import sucesso, erro
from app.auth.decorators import perfil_requerido

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# ---------------------------------------------------------------------------
# Usuários (Administrador, Professor, Responsável)
# ---------------------------------------------------------------------------

@admin_bp.get("/usuarios")
@perfil_requerido("admin")
def listar_usuarios():
    perfil_filtro = request.args.get("perfil")
    query = Usuario.query
    if perfil_filtro:
        query = query.filter_by(perfil=perfil_filtro)
    usuarios = query.order_by(Usuario.nome).all()
    return sucesso(dados=[u.to_dict() for u in usuarios])


@admin_bp.post("/usuarios")
@perfil_requerido("admin")
def criar_usuario():
    payload = request.get_json(silent=True) or {}
    nome = (payload.get("nome") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    senha = payload.get("senha") or ""
    perfil = payload.get("perfil") or ""

    if not nome or not email or not senha:
        return erro("Nome, e-mail e senha são obrigatórios.", status=400)
    if perfil not in PERFIS_VALIDOS:
        return erro(f"Perfil inválido. Use um de: {', '.join(PERFIS_VALIDOS)}.", status=400)
    if len(senha) < 6:
        return erro("A senha deve ter pelo menos 6 caracteres.", status=400)
    if Usuario.query.filter_by(email=email).first():
        return erro("Já existe um usuário com este e-mail.", status=409)

    usuario = Usuario(nome=nome, email=email, perfil=perfil)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()
    return sucesso(dados=usuario.to_dict(), mensagem="Usuário criado com sucesso.", status=201)


@admin_bp.put("/usuarios/<int:usuario_id>")
@perfil_requerido("admin")
def atualizar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return erro("Usuário não encontrado.", status=404)

    payload = request.get_json(silent=True) or {}
    if "nome" in payload:
        usuario.nome = (payload["nome"] or "").strip() or usuario.nome
    if "ativo" in payload:
        usuario.ativo = bool(payload["ativo"])
    if payload.get("senha"):
        if len(payload["senha"]) < 6:
            return erro("A senha deve ter pelo menos 6 caracteres.", status=400)
        usuario.set_senha(payload["senha"])

    db.session.commit()
    return sucesso(dados=usuario.to_dict(), mensagem="Usuário atualizado com sucesso.")


@admin_bp.delete("/usuarios/<int:usuario_id>")
@perfil_requerido("admin")
def desativar_usuario(usuario_id):
    """Desativação lógica (não apagamos o histórico do usuário do banco)."""
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return erro("Usuário não encontrado.", status=404)
    usuario.ativo = False
    db.session.commit()
    return sucesso(mensagem="Usuário desativado com sucesso.")


# ---------------------------------------------------------------------------
# Turmas
# ---------------------------------------------------------------------------

@admin_bp.get("/turmas")
@perfil_requerido("admin", "professor")
def listar_turmas():
    turmas = Turma.query.order_by(Turma.ano_letivo.desc(), Turma.nome).all()
    return sucesso(dados=[t.to_dict() for t in turmas])


@admin_bp.post("/turmas")
@perfil_requerido("admin")
def criar_turma():
    payload = request.get_json(silent=True) or {}
    nome = (payload.get("nome") or "").strip()
    ano_letivo = payload.get("ano_letivo")

    if not nome:
        return erro("Nome da turma é obrigatório.", status=400)
    if not isinstance(ano_letivo, int) or ano_letivo < 2000:
        return erro("Ano letivo inválido.", status=400)

    turma = Turma(nome=nome, ano_letivo=ano_letivo)
    db.session.add(turma)
    db.session.commit()
    return sucesso(dados=turma.to_dict(), mensagem="Turma criada com sucesso.", status=201)


@admin_bp.get("/turmas/<int:turma_id>")
@perfil_requerido("admin", "professor")
def detalhar_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return erro("Turma não encontrada.", status=404)
    return sucesso(dados=turma.to_dict(incluir_alunos=True))


@admin_bp.post("/turmas/<int:turma_id>/alunos")
@perfil_requerido("admin")
def adicionar_aluno_na_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return erro("Turma não encontrada.", status=404)

    payload = request.get_json(silent=True) or {}
    nome = (payload.get("nome") or "").strip()
    matricula = (payload.get("matricula") or "").strip()
    data_nascimento_str = payload.get("data_nascimento")  # "YYYY-MM-DD"

    if not nome or not matricula:
        return erro("Nome e matrícula do aluno são obrigatórios.", status=400)
    if Aluno.query.filter_by(matricula=matricula).first():
        return erro("Já existe um aluno cadastrado com esta matrícula.", status=409)

    data_nascimento = None
    if data_nascimento_str:
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
        except ValueError:
            return erro("Data de nascimento inválida. Use o formato AAAA-MM-DD.", status=400)

    aluno = Aluno(
        nome=nome, matricula=matricula, data_nascimento=data_nascimento, turma_id=turma.id,
    )
    db.session.add(aluno)
    db.session.commit()
    return sucesso(dados=aluno.to_dict(), mensagem="Aluno cadastrado na turma.", status=201)


@admin_bp.post("/turmas/<int:turma_id>/vincular-professor")
@perfil_requerido("admin")
def vincular_professor_disciplina(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return erro("Turma não encontrada.", status=404)

    payload = request.get_json(silent=True) or {}
    professor_id = payload.get("professor_id")
    disciplina_nome = (payload.get("disciplina") or "").strip()

    professor = Usuario.query.filter_by(id=professor_id, perfil="professor").first()
    if not professor:
        return erro("Professor não encontrado.", status=404)
    if not disciplina_nome:
        return erro("Informe o nome da disciplina.", status=400)

    disciplina = Disciplina.query.filter_by(nome=disciplina_nome).first()
    if not disciplina:
        disciplina = Disciplina(nome=disciplina_nome)
        db.session.add(disciplina)
        db.session.flush()

    ja_existe = TurmaDisciplinaProfessor.query.filter_by(
        turma_id=turma.id, disciplina_id=disciplina.id, professor_id=professor.id
    ).first()
    if ja_existe:
        return erro("Este professor já está vinculado a esta disciplina nesta turma.", status=409)

    vinculo = TurmaDisciplinaProfessor(
        turma_id=turma.id, disciplina_id=disciplina.id, professor_id=professor.id
    )
    db.session.add(vinculo)
    db.session.commit()
    return sucesso(dados=vinculo.to_dict(), mensagem="Vínculo criado com sucesso.", status=201)


@admin_bp.post("/vincular-responsavel")
@perfil_requerido("admin")
def vincular_responsavel_aluno():
    payload = request.get_json(silent=True) or {}
    responsavel_id = payload.get("responsavel_id")
    aluno_id = payload.get("aluno_id")
    parentesco = (payload.get("parentesco") or "").strip() or None

    responsavel = Usuario.query.filter_by(id=responsavel_id, perfil="responsavel").first()
    if not responsavel:
        return erro("Responsável não encontrado.", status=404)
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return erro("Aluno não encontrado.", status=404)

    ja_existe = ResponsavelAluno.query.filter_by(
        responsavel_id=responsavel.id, aluno_id=aluno.id
    ).first()
    if ja_existe:
        return erro("Este responsável já está vinculado a este aluno.", status=409)

    vinculo = ResponsavelAluno(
        responsavel_id=responsavel.id, aluno_id=aluno.id, parentesco=parentesco
    )
    db.session.add(vinculo)
    db.session.commit()
    return sucesso(mensagem="Responsável vinculado ao aluno com sucesso.", status=201)


# ---------------------------------------------------------------------------
# Histórico escolar (importação simplificada de alunos transferidos)
# ---------------------------------------------------------------------------

@admin_bp.post("/historico/importar")
@perfil_requerido("admin")
def importar_historico():
    """
    Importa em lote notas e faltas de um aluno vindo de outra escola.
    Espera um JSON no formato:
    {
      "aluno_id": 1,
      "notas": [{"disciplina": "Matemática", "valor": 8.5, "etapa": "1º Bimestre"}],
      "faltas": [{"data_falta": "2025-03-10", "justificada": true, "motivo_justificativa": "..."}]
    }
    """
    payload = request.get_json(silent=True) or {}
    aluno = Aluno.query.get(payload.get("aluno_id"))
    if not aluno:
        return erro("Aluno não encontrado.", status=404)

    importadas_notas, importadas_faltas = 0, 0

    for item in payload.get("notas", []):
        disciplina = Disciplina.query.filter_by(nome=item.get("disciplina", "").strip()).first()
        if not disciplina:
            disciplina = Disciplina(nome=item.get("disciplina", "").strip())
            db.session.add(disciplina)
            db.session.flush()
        try:
            valor = Nota.validar_valor(item.get("valor"))
        except ValueError:
            continue
        db.session.add(Nota(
            aluno_id=aluno.id, turma_id=aluno.turma_id, disciplina_id=disciplina.id,
            professor_id=None, valor=valor, etapa=item.get("etapa"),
        ))
        importadas_notas += 1

    for item in payload.get("faltas", []):
        try:
            data_falta = datetime.strptime(item["data_falta"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            continue
        db.session.add(Falta(
            aluno_id=aluno.id, turma_id=aluno.turma_id, data_falta=data_falta,
            justificada=bool(item.get("justificada", False)),
            motivo_justificativa=item.get("motivo_justificativa"),
        ))
        importadas_faltas += 1

    db.session.commit()
    return sucesso(
        dados={"notas_importadas": importadas_notas, "faltas_importadas": importadas_faltas},
        mensagem="Histórico importado com sucesso.",
    )


# ---------------------------------------------------------------------------
# Dashboard administrativo
# ---------------------------------------------------------------------------

@admin_bp.get("/dashboard")
@perfil_requerido("admin")
def dashboard():
    return sucesso(dados={
        "total_turmas": Turma.query.count(),
        "total_alunos": Aluno.query.filter_by(ativo=True).count(),
        "total_professores": Usuario.query.filter_by(perfil="professor", ativo=True).count(),
        "total_responsaveis": Usuario.query.filter_by(perfil="responsavel", ativo=True).count(),
        "documentos_pendentes": Documento.query.filter_by(status="pendente").count(),
    })
