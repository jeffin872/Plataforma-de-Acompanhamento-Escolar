from datetime import date

from app.extensions import db


class Nota(db.Model):
    __tablename__ = "notas"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    # Nulo apenas quando a nota vem de importação de histórico escolar (ver
    # admin/routes.py -> importar_historico), sem professor desta escola envolvido.
    professor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)

    valor = db.Column(db.Float, nullable=False)
    etapa = db.Column(db.String(30), nullable=True)  # ex: "1º Bimestre"
    data_avaliacao = db.Column(db.Date, nullable=False, default=date.today)

    aluno = db.relationship("Aluno", back_populates="notas")
    turma = db.relationship("Turma")
    disciplina = db.relationship("Disciplina")
    professor = db.relationship("Usuario")

    @staticmethod
    def validar_valor(valor: float) -> float:
        if not isinstance(valor, (int, float)):
            raise ValueError("Nota deve ser numérica.")
        if valor < 0 or valor > 10:
            raise ValueError("Nota deve estar entre 0 e 10.")
        return float(valor)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "aluno_nome": self.aluno.nome if self.aluno else None,
            "turma_id": self.turma_id,
            "disciplina": self.disciplina.to_dict() if self.disciplina else None,
            "professor": self.professor.nome if self.professor else None,
            "valor": self.valor,
            "etapa": self.etapa,
            "data_avaliacao": self.data_avaliacao.isoformat() if self.data_avaliacao else None,
        }
