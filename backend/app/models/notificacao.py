from datetime import datetime, timezone

from app.extensions import db


class Notificacao(db.Model):
    """
    Registro interno (para exibir um "sininho" no painel do responsável)
    de todo alerta disparado pelo módulo de Alertas e Notificações -
    ver app/alerts/service.py. O e-mail é apenas um canal a mais.
    """
    __tablename__ = "notificacoes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    tipo = db.Column(db.String(40), nullable=False)  # ex: "excesso_faltas", "documento_analisado"
    mensagem = db.Column(db.String(255), nullable=False)
    lida = db.Column(db.Boolean, nullable=False, default=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = db.relationship("Usuario", back_populates="notificacoes")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.tipo,
            "mensagem": self.mensagem,
            "lida": self.lida,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
