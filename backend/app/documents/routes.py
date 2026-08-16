from flask import Blueprint, request, send_from_directory, current_app

from app.extensions import db
from app.models import Documento, ResponsavelAluno, Aluno, Notificacao
from app.models.documento import STATUS_VALIDOS
from app.utils.responses import sucesso, erro
from app.auth.decorators import perfil_requerido, usuario_logado_id
from app.documents.storage import get_storage, extensao_permitida

documents_bp = Blueprint("documents", __name__, url_prefix="/api/documentos")


@documents_bp.post("")
@perfil_requerido("responsavel")
def enviar_documento():
    """Responsável anexa um documento (ex: atestado) para um aluno vinculado a ele."""
    responsavel_id = usuario_logado_id()
    aluno_id = request.form.get("aluno_id", type=int)
    tipo = request.form.get("tipo", "atestado")
    arquivo = request.files.get("arquivo")

    vinculo = ResponsavelAluno.query.filter_by(
        responsavel_id=responsavel_id, aluno_id=aluno_id
    ).first()
    if not vinculo:
        return erro("Este aluno não está vinculado a você.", status=403)
    if not arquivo or arquivo.filename == "":
        return erro("Anexe um arquivo.", status=400)
    if not extensao_permitida(arquivo.filename):
        return erro("Formato de arquivo não permitido. Use PDF, PNG ou JPG.", status=400)

    url_arquivo = get_storage().salvar(arquivo, arquivo.filename)

    documento = Documento(
        aluno_id=aluno_id,
        responsavel_id=responsavel_id,
        tipo=tipo,
        nome_arquivo_original=arquivo.filename,
        url_arquivo=url_arquivo,
        status="pendente",
    )
    db.session.add(documento)
    db.session.commit()
    return sucesso(
        dados=documento.to_dict(), mensagem="Documento enviado. Aguarde a análise da escola.",
        status=201,
    )


@documents_bp.get("/arquivo/<path:nome_arquivo>")
@perfil_requerido("admin", "professor", "responsavel")
def baixar_arquivo_local(nome_arquivo):
    """Serve o arquivo quando STORAGE_BACKEND=local (em produção com S3 isso não é usado)."""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], nome_arquivo)


@documents_bp.get("/meus")
@perfil_requerido("responsavel")
def meus_documentos():
    documentos = (
        Documento.query.filter_by(responsavel_id=usuario_logado_id())
        .order_by(Documento.enviado_em.desc())
        .all()
    )
    return sucesso(dados=[d.to_dict() for d in documentos])


@documents_bp.get("")
@perfil_requerido("admin", "professor")
def listar_documentos():
    """Fila de análise para a escola: por padrão só mostra os pendentes."""
    status_filtro = request.args.get("status", "pendente")
    query = Documento.query
    if status_filtro in STATUS_VALIDOS:
        query = query.filter_by(status=status_filtro)
    documentos = query.order_by(Documento.enviado_em.desc()).all()
    return sucesso(dados=[d.to_dict() for d in documentos])


@documents_bp.put("/<int:documento_id>")
@perfil_requerido("admin", "professor")
def revisar_documento(documento_id):
    documento = Documento.query.get(documento_id)
    if not documento:
        return erro("Documento não encontrado.", status=404)

    payload = request.get_json(silent=True) or {}
    novo_status = payload.get("status")
    observacao = payload.get("observacao")

    try:
        documento.revisar(novo_status, usuario_logado_id(), observacao)
    except ValueError as exc:
        return erro(str(exc), status=400)

    # Avisa o responsável (dentro do sistema) que o documento foi analisado.
    db.session.add(Notificacao(
        usuario_id=documento.responsavel_id,
        tipo="documento_analisado",
        mensagem=(
            f"O documento '{documento.nome_arquivo_original}' enviado para "
            f"{documento.aluno.nome} foi {novo_status}."
        ),
    ))
    db.session.commit()
    return sucesso(dados=documento.to_dict(), mensagem="Documento revisado com sucesso.")
