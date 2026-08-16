"""
Reúne todos os models num único ponto de import. Isso garante que o
Flask-Migrate enxergue todas as tabelas na hora de gerar as migrations
(basta um `from app import models` acontecer antes do `flask db migrate`).
"""
from app.models.usuario import Usuario
from app.models.academico import Turma, Disciplina, TurmaDisciplinaProfessor
from app.models.aluno import Aluno, ResponsavelAluno
from app.models.nota import Nota
from app.models.falta import Falta
from app.models.ocorrencia import Ocorrencia
from app.models.documento import Documento
from app.models.notificacao import Notificacao

__all__ = [
    "Usuario",
    "Turma",
    "Disciplina",
    "TurmaDisciplinaProfessor",
    "Aluno",
    "ResponsavelAluno",
    "Nota",
    "Falta",
    "Ocorrencia",
    "Documento",
    "Notificacao",
]
