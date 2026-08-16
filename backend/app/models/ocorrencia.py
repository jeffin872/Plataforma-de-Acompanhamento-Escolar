from datetime import datetime, timezone, date

from app.extensions import db

TIPOS_OCORRENCIA = ("elogio", "advertencia", "observacao", "encaminhamento")


class Ocorrencia(db.Model):
    __tablename__ = "ocorrencias"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    tipo = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_ocorrencia = db.Column(db.Date, nullable=False, default=date.today)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    aluno = db.relationship("Aluno", back_populates="ocorrencias")
    turma = db.relationship("Turma")
    professor = db.relationship("Usuario")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "aluno_nome": self.aluno.nome if self.aluno else None,
            "turma_id": self.turma_id,
            "professor": self.professor.nome if self.professor else None,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "data_ocorrencia": self.data_ocorrencia.isoformat() if self.data_ocorrencia else None,
        }
