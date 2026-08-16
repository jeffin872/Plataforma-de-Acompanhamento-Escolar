"""
Popula o banco com um conjunto mínimo de dados para dar pra testar o
sistema de ponta a ponta (login de cada perfil, turma com aluno, etc).

Uso:
    python seed.py

Rode só depois de `flask db upgrade` (banco já com as tabelas criadas).
"""
from datetime import date

from app import create_app
from app.extensions import db
from app.models import (
    Usuario, Turma, Disciplina, TurmaDisciplinaProfessor, Aluno, ResponsavelAluno,
)

app = create_app()

with app.app_context():
    if Usuario.query.filter_by(email="admin@escola.com").first():
        print("Seed já foi executado antes (admin@escola.com já existe). Nada a fazer.")
        raise SystemExit(0)

    admin = Usuario(nome="Ana Diretora", email="admin@escola.com", perfil="admin")
    admin.set_senha("admin123")

    professor = Usuario(nome="Maria Oliveira", email="professor@escola.com", perfil="professor")
    professor.set_senha("professor123")

    responsavel = Usuario(nome="João Silva", email="responsavel@escola.com", perfil="responsavel")
    responsavel.set_senha("responsavel123")

    db.session.add_all([admin, professor, responsavel])
    db.session.flush()  # garante os IDs antes de usar nas relações abaixo

    turma = Turma(nome="9º Ano A", ano_letivo=2026)
    disciplina = Disciplina(nome="Matemática")
    db.session.add_all([turma, disciplina])
    db.session.flush()

    aluno = Aluno(
        nome="Carlos Silva", matricula="2026001",
        data_nascimento=date(2011, 5, 20), turma_id=turma.id,
    )
    db.session.add(aluno)
    db.session.flush()

    db.session.add(TurmaDisciplinaProfessor(
        turma_id=turma.id, disciplina_id=disciplina.id, professor_id=professor.id,
    ))
    db.session.add(ResponsavelAluno(
        responsavel_id=responsavel.id, aluno_id=aluno.id, parentesco="pai",
    ))

    db.session.commit()

    print("Seed concluído! Usuários de teste:")
    print("  Admin:       admin@escola.com       / admin123")
    print("  Professor:   professor@escola.com   / professor123")
    print("  Responsável: responsavel@escola.com / responsavel123")
    print(f"Turma '{turma.nome}' criada com o aluno '{aluno.nome}' (matrícula {aluno.matricula}).")
