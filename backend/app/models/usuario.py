from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

PERFIS_VALIDOS = ("admin", "professor", "responsavel")


class Usuario(db.Model):
    """
    Tabela única de usuários do sistema. O campo `perfil` define o que a
    pessoa pode acessar (Administrador, Professor ou Responsável), seguindo
    a "Separação por Perfil" definida na documentação do projeto.
    """
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    alunos_vinculados = db.relationship(
        "ResponsavelAluno", back_populates="responsavel", cascade="all, delete-orphan"
    )
    documentos_enviados = db.relationship(
        "Documento", back_populates="responsavel", foreign_keys="Documento.responsavel_id"
    )
    notificacoes = db.relationship(
        "Notificacao", back_populates="usuario", cascade="all, delete-orphan"
    )

    def set_senha(self, senha_texto_puro: str) -> None:
        """Nunca guardamos a senha em texto puro, apenas o hash."""
        self.senha_hash = generate_password_hash(senha_texto_puro)

    def checar_senha(self, senha_texto_puro: str) -> bool:
        return check_password_hash(self.senha_hash, senha_texto_puro)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "perfil": self.perfil,
            "ativo": self.ativo,
        }

    def __repr__(self) -> str:
        return f"<Usuario {self.email} ({self.perfil})>"
