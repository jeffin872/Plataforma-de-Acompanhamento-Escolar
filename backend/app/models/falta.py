from datetime import date

from app.extensions import db


class Falta(db.Model):
    __tablename__ = "faltas"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=True)
    data_falta = db.Column(db.Date, nullable=False, default=date.today)
    justificada = db.Column(db.Boolean, nullable=False, default=False)
    motivo_justificativa = db.Column(db.String(255), nullable=True)

    aluno = db.relationship("Aluno", back_populates="faltas")
    turma = db.relationship("Turma")

    def justificar(self, motivo: str) -> None:
        motivo = (motivo or "").strip()
        if not motivo:
            raise ValueError("Informe um motivo para justificar a falta.")
        self.justificada = True
        self.motivo_justificativa = motivo

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "aluno_nome": self.aluno.nome if self.aluno else None,
            "turma_id": self.turma_id,
            "data_falta": self.data_falta.isoformat() if self.data_falta else None,
            "justificada": self.justificada,
            "motivo_justificativa": self.motivo_justificativa,
        }
