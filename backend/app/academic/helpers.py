from app.models import TurmaDisciplinaProfessor


def professor_pode_lecionar(professor_id: int, turma_id: int, disciplina_id: int) -> bool:
    """
    Espelha a regra que já existia no protótipo Python do EP1
    (Turma.tem_professor_disciplina): só quem está formalmente vinculado
    à turma+disciplina pode lançar notas, faltas ou ocorrências nela.
    """
    vinculo = TurmaDisciplinaProfessor.query.filter_by(
        professor_id=professor_id, turma_id=turma_id, disciplina_id=disciplina_id
    ).first()
    return vinculo is not None


def aluno_pertence_a_turma(aluno, turma_id: int) -> bool:
    return aluno is not None and aluno.turma_id == turma_id
