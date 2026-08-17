"""
Fluxo de ponta a ponta "Gestão de Faltas e Atestados", envolvendo os 3
perfis do sistema:

  1) Professor  -> registra uma falta (nasce "Pendente")
  2) Responsável -> envia um atestado vinculado à falta ("Em Análise")
  3) Administrador -> aprova ("Justificada") ou rejeita (volta "Pendente")

Armazenamento em memória (ver app/fluxo_faltas/store.py) — não grava no
PostgreSQL. Os únicos acessos ao banco aqui são leituras pontuais em
`Aluno`/`Usuario` já existentes, só para validar que o aluno/usuário é
real e exibir nome nas respostas; nenhuma tabela nova foi criada.
"""
from flask import Blueprint, request

from app.models import Aluno, Usuario
from app.utils.responses import sucesso, erro
from app.auth.decorators import perfil_requerido, usuario_logado_id
from app.documents.storage import get_storage, extensao_permitida
from app.fluxo_faltas.store import (
    FALTAS,
    ATESTADOS,
    agora_iso,
    proximo_id_falta,
    proximo_id_atestado,
    buscar_falta,
    buscar_atestado,
)

STATUS_FALTA_VALIDOS = ("Pendente", "Em Análise", "Justificada")

# ===========================================================================
# 1) Professor — registrar falta
# ===========================================================================
professor_faltas_bp = Blueprint(
    "professor_faltas_mvp", __name__, url_prefix="/api/professor"
)


@professor_faltas_bp.get("/faltas")
@perfil_requerido("professor", "admin")
def listar_faltas_mvp():
    """
    Lista as faltas registradas neste fluxo, mais recentes primeiro.
    Filtros opcionais via query string: ?aluno_id=1&status=Pendente
    """
    aluno_id = request.args.get("aluno_id", type=int)
    status = request.args.get("status")

    resultado = FALTAS
    if aluno_id:
        resultado = [f for f in resultado if f["aluno_id"] == aluno_id]
    if status:
        resultado = [f for f in resultado if f["status"].lower() == status.lower()]

    resultado = sorted(resultado, key=lambda f: f["id"], reverse=True)
    return sucesso(dados=resultado)


@professor_faltas_bp.post("/faltas")
@perfil_requerido("professor")
def registrar_falta_mvp():
    """
    Registra uma falta com status inicial "Pendente".
    Corpo esperado (JSON): { "aluno_id": int, "data": "AAAA-MM-DD", "disciplina": str }
    """
    payload = request.get_json(silent=True) or {}
    aluno_id = payload.get("aluno_id")
    data_falta = (payload.get("data") or "").strip()
    disciplina = (payload.get("disciplina") or "").strip()

    if not aluno_id:
        return erro("Informe o aluno.", status=400)
    if not data_falta:
        return erro("Informe a data da falta.", status=400)
    if not disciplina:
        return erro("Informe a disciplina.", status=400)

    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return erro("Aluno não encontrado.", status=404)

    falta = {
        "id": proximo_id_falta(),
        "aluno_id": aluno.id,
        "aluno_nome": aluno.nome,
        "disciplina": disciplina,
        "data": data_falta,
        "status": "Pendente",
        "professor_id": usuario_logado_id(),
        "registrado_em": agora_iso(),
    }
    FALTAS.append(falta)
    return sucesso(dados=falta, mensagem="Falta registrada com sucesso.", status=201)


# ===========================================================================
# 2) Responsável — enviar atestado (justifica uma falta específica)
# ===========================================================================
documentos_atestados_bp = Blueprint(
    "documentos_atestados_mvp", __name__, url_prefix="/api/documentos"
)


@documentos_atestados_bp.get("/faltas/<int:aluno_id>")
@perfil_requerido("responsavel", "admin", "professor")
def listar_faltas_do_aluno_mvp(aluno_id):
    """
    Lista as faltas (deste fluxo) de um aluno específico — usado pelo
    Responsável para escolher, num <select>, qual falta está justificando.
    Filtro opcional: ?status=Pendente
    """
    status = request.args.get("status")
    resultado = [f for f in FALTAS if f["aluno_id"] == aluno_id]
    if status:
        resultado = [f for f in resultado if f["status"].lower() == status.lower()]
    resultado = sorted(resultado, key=lambda f: f["id"], reverse=True)
    return sucesso(dados=resultado)


@documentos_atestados_bp.post("/upload")
@perfil_requerido("responsavel")
def upload_atestado_mvp():
    """
    Vincula um atestado a uma falta específica e muda o status dela para
    "Em Análise". Aceita multipart/form-data (campo "arquivo" + "falta_id"),
    que é o que o formulário de upload do frontend envia.

    O arquivo é gravado de verdade (reaproveitando o mesmo serviço de
    armazenamento do fluxo "oficial" de documentos, ver
    app/documents/storage.py), para que o Administrador consiga abrir e
    conferir o atestado na tela de validação.
    """
    responsavel_id = usuario_logado_id()
    arquivo = None

    if request.content_type and "multipart/form-data" in request.content_type:
        falta_id = request.form.get("falta_id", type=int)
        arquivo = request.files.get("arquivo")
        nome_arquivo = arquivo.filename if arquivo and arquivo.filename else None
        if nome_arquivo and not extensao_permitida(nome_arquivo):
            return erro("Formato de arquivo não permitido. Use PDF, PNG ou JPG.", status=400)
    else:
        payload = request.get_json(silent=True) or {}
        falta_id = payload.get("falta_id")
        nome_arquivo = payload.get("nome_arquivo") or (
            "atestado.pdf" if payload.get("arquivo_base64") else None
        )

    if not falta_id:
        return erro("Informe a falta que está sendo justificada.", status=400)
    if not nome_arquivo:
        return erro("Selecione o arquivo do atestado.", status=400)

    falta = buscar_falta(int(falta_id))
    if not falta:
        return erro("Falta não encontrada.", status=404)
    if falta["aluno_id"] not in [
        a.aluno_id
        for a in Usuario.query.get(responsavel_id).alunos_vinculados
    ]:
        return erro("Esta falta não pertence a um aluno vinculado a você.", status=403)
    if falta["status"] == "Justificada":
        return erro("Esta falta já foi justificada.", status=409)
    if falta["status"] == "Em Análise":
        return erro("Já existe um atestado em análise para esta falta.", status=409)

    responsavel = Usuario.query.get(responsavel_id)

    # Só existe arquivo de verdade pra salvar quando o envio veio como
    # multipart (o caminho JSON com "arquivo_base64" é um atalho legado
    # só para testes manuais de API e não grava nada em disco).
    url_arquivo = get_storage().salvar(arquivo, nome_arquivo) if arquivo else None

    atestado = {
        "id": proximo_id_atestado(),
        "falta_id": falta["id"],
        "aluno_id": falta["aluno_id"],
        "aluno_nome": falta["aluno_nome"],
        "disciplina": falta["disciplina"],
        "data_falta": falta["data"],
        "responsavel_id": responsavel_id,
        "responsavel_nome": responsavel.nome if responsavel else None,
        "nome_arquivo": nome_arquivo,
        "url_arquivo": url_arquivo,
        "status": "Em Análise",
        "observacao": None,
        "enviado_em": agora_iso(),
        "analisado_em": None,
    }
    ATESTADOS.append(atestado)
    falta["status"] = "Em Análise"

    return sucesso(dados=atestado, mensagem="Atestado enviado para análise.", status=201)


# ===========================================================================
# 3) Administrador — analisar e validar atestados
# ===========================================================================
admin_atestados_bp = Blueprint("admin_atestados_mvp", __name__, url_prefix="/api/admin")


@admin_atestados_bp.get("/documentos/pendentes")
@perfil_requerido("admin")
def listar_atestados_pendentes_mvp():
    """
    Lista os atestados enviados. Por padrão devolve só os "Em Análise";
    passe ?status=todos para ver o histórico completo (aprovados/rejeitados).
    """
    status = request.args.get("status", "Em Análise")
    resultado = ATESTADOS
    if status.lower() != "todos":
        resultado = [a for a in ATESTADOS if a["status"].lower() == status.lower()]
    resultado = sorted(resultado, key=lambda a: a["id"], reverse=True)
    return sucesso(dados=resultado)


@admin_atestados_bp.post("/documentos/validar")
@perfil_requerido("admin")
def validar_atestado_mvp():
    """
    Corpo esperado (JSON):
      { "atestado_id": int, "acao": "aprovar" | "rejeitar", "observacao": str? }

    Se aprovado: a falta vinculada ganha o status "Justificada".
    Se rejeitado: a falta volta para "Pendente" (o responsável pode reenviar).
    """
    payload = request.get_json(silent=True) or {}
    atestado_id = payload.get("atestado_id")
    acao = (payload.get("acao") or "").strip().lower()
    observacao = (payload.get("observacao") or "").strip() or None

    if acao not in ("aprovar", "rejeitar"):
        return erro("Ação inválida. Use 'aprovar' ou 'rejeitar'.", status=400)

    atestado = buscar_atestado(atestado_id)
    if not atestado:
        return erro("Atestado não encontrado.", status=404)
    if atestado["status"] != "Em Análise":
        return erro("Este atestado já foi analisado.", status=409)

    falta = buscar_falta(atestado["falta_id"])

    if acao == "aprovar":
        atestado["status"] = "Aprovado"
        if falta:
            falta["status"] = "Justificada"
        mensagem = "Atestado aprovado. A falta foi justificada."
    else:
        atestado["status"] = "Rejeitado"
        if falta:
            falta["status"] = "Pendente"
        mensagem = "Atestado rejeitado. A falta voltou para pendente."

    atestado["observacao"] = observacao
    atestado["analisado_em"] = agora_iso()
    atestado["analisado_por_id"] = usuario_logado_id()

    return sucesso(dados=atestado, mensagem=mensagem)
