from datetime import date

from app.extensions import db


class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    matricula = db.Column(db.String(30), nullable=False, unique=True, index=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=True)

    turma = db.relationship("Turma", back_populates="alunos")
    responsaveis = db.relationship(
        "ResponsavelAluno", back_populates="aluno", cascade="all, delete-orphan"
    )
    notas = db.relationship("Nota", back_populates="aluno", cascade="all, delete-orphan")
    faltas = db.relationship("Falta", back_populates="aluno", cascade="all, delete-orphan")
    ocorrencias = db.relationship(
        "Ocorrencia", back_populates="aluno", cascade="all, delete-orphan"
    )
    documentos = db.relationship(
        "Documento", back_populates="aluno", cascade="all, delete-orphan"
    )

    def idade(self):
        if not self.data_nascimento:
            return None
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "matricula": self.matricula,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "idade": self.idade(),
            "ativo": self.ativo,
            "turma": self.turma.to_dict() if self.turma else None,
        }


class ResponsavelAluno(db.Model):
    """
    Um responsável pode acompanhar mais de um aluno (ex: irmãos) e, em
    tese, um aluno pode ter mais de um responsável cadastrado (mãe e pai,
    por exemplo). Por isso o vínculo é feito numa tabela associativa.
    """
    __tablename__ = "responsavel_aluno"
    __table_args__ = (
        db.UniqueConstraint("responsavel_id", "aluno_id", name="uq_responsavel_aluno"),
    )

    id = db.Column(db.Integer, primary_key=True)
    responsavel_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    parentesco = db.Column(db.String(40), nullable=True)  # ex: "mãe", "pai", "avó"

    responsavel = db.relationship("Usuario", back_populates="alunos_vinculados")
    aluno = db.relationship("Aluno", back_populates="responsaveis")
