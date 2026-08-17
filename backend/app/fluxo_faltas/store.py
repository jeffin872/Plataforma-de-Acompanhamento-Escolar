"""
Armazenamento em memória do fluxo "Gestão de Faltas e Atestados".

Por pedido explícito do time, este fluxo NÃO usa o banco de dados
(SQLAlchemy/PostgreSQL) real do projeto — os dados vivem só na memória
do processo Flask (listas Python), servindo puramente para demonstrar o
MVP de ponta a ponta. Reiniciar o servidor apaga tudo aqui, por design.

Isso é intencionalmente separado do fluxo "de verdade" já existente em
app/academic (Falta) e app/documents (Documento), que continuam
intactos e gravando no PostgreSQL normalmente.
"""
import itertools
from datetime import datetime, timezone

# --- "Tabelas" em memória ---
FALTAS = []
ATESTADOS = []

_contador_falta_id = itertools.count(1)
_contador_atestado_id = itertools.count(1)


def agora_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def proximo_id_falta() -> int:
    return next(_contador_falta_id)


def proximo_id_atestado() -> int:
    return next(_contador_atestado_id)


def buscar_falta(falta_id):
    return next((f for f in FALTAS if f["id"] == falta_id), None)


def buscar_atestado(atestado_id):
    return next((a for a in ATESTADOS if a["id"] == atestado_id), None)
