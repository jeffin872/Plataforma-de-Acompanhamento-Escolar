from datetime import datetime, timezone

from app.extensions import db

STATUS_VALIDOS = ("pendente", "aprovado", "rejeitado")


class Documento(db.Model):
    """
    Representa um documento (ex: atestado médico) enviado pelo responsável.
    O arquivo em si não fica salvo no banco: só a URL/caminho devolvido pelo
    serviço de armazenamento (local em dev, nuvem em produção) - ver
    app/documents/storage.py.
    """
    __tablename__ = "documentos"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    tipo = db.Column(db.String(50), nullable=False, default="atestado")
    nome_arquivo_original = db.Column(db.String(255), nullable=False)
    url_arquivo = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    observacao_analise = db.Column(db.String(255), nullable=True)

    enviado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    analisado_em = db.Column(db.DateTime, nullable=True)
    analisado_por_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)

    aluno = db.relationship("Aluno", back_populates="documentos")
    responsavel = db.relationship(
        "Usuario", back_populates="documentos_enviados", foreign_keys=[responsavel_id]
    )
    analisado_por = db.relationship("Usuario", foreign_keys=[analisado_por_id])

    def revisar(self, novo_status: str, usuario_id: int, observacao: str = None) -> None:
        if novo_status not in ("aprovado", "rejeitado"):
            raise ValueError("Status de revisão inválido.")
        self.status = novo_status
        self.analisado_por_id = usuario_id
        self.observacao_analise = observacao
        self.analisado_em = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "aluno_nome": self.aluno.nome if self.aluno else None,
            "responsavel_nome": self.responsavel.nome if self.responsavel else None,
            "tipo": self.tipo,
            "nome_arquivo_original": self.nome_arquivo_original,
            "url_arquivo": self.url_arquivo,
            "status": self.status,
            "observacao_analise": self.observacao_analise,
            "enviado_em": self.enviado_em.isoformat() if self.enviado_em else None,
            "analisado_em": self.analisado_em.isoformat() if self.analisado_em else None,
        }
