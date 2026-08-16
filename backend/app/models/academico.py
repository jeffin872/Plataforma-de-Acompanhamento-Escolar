from app.extensions import db


class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    ano_letivo = db.Column(db.Integer, nullable=False)

    alunos = db.relationship("Aluno", back_populates="turma")
    vinculos_professor = db.relationship(
        "TurmaDisciplinaProfessor", back_populates="turma", cascade="all, delete-orphan"
    )

    def to_dict(self, incluir_alunos=False) -> dict:
        dados = {
            "id": self.id,
            "nome": self.nome,
            "ano_letivo": self.ano_letivo,
            "total_alunos": len(self.alunos),
        }
        if incluir_alunos:
            dados["alunos"] = [a.to_dict() for a in self.alunos]
        return dados


class Disciplina(db.Model):
    __tablename__ = "disciplinas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)

    def to_dict(self) -> dict:
        return {"id": self.id, "nome": self.nome}


class TurmaDisciplinaProfessor(db.Model):
    """
    Vínculo entre professor, disciplina e turma: define quem pode lançar
    notas/faltas de qual disciplina em qual turma. Sem esse registro, o
    backend recusa o lançamento (mesma regra que já existia no protótipo
    em Python puro do EP1 - Turma.tem_professor_disciplina()).
    """
    __tablename__ = "turma_disciplina_professor"
    __table_args__ = (
        db.UniqueConstraint("turma_id", "disciplina_id", "professor_id", name="uq_vinculo_prof"),
    )

    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    turma = db.relationship("Turma", back_populates="vinculos_professor")
    disciplina = db.relationship("Disciplina")
    professor = db.relationship("Usuario")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "turma": self.turma.to_dict(),
            "disciplina": self.disciplina.to_dict(),
            "professor": self.professor.to_dict(),
        }
