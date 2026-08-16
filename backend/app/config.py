"""
Configurações centrais da aplicação.

Todas as variáveis sensíveis (senhas, chaves, credenciais) vêm do arquivo .env
e NUNCA devem ser escritas direto no código-fonte.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

# Carrega o .env que fica na raiz do projeto backend/
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    # --- Flask ---
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # --- Banco de Dados ---
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/acompanhamento_escolar",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- JWT ---
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "60"))
    )

    # --- CORS ---
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    # --- Armazenamento de documentos ---
    STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "instance", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB por arquivo enviado

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")
    AWS_S3_REGION = os.getenv("AWS_S3_REGION", "us-east-1")

    # --- E-mail / Alertas ---
    EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "console")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "alertas@escola.com")

    # --- Regras de negócio ---
    LIMITE_FALTAS_ALERTA = int(os.getenv("LIMITE_FALTAS_ALERTA", "5"))


class TestingConfig(Config):
    """Usada nos testes automatizados e no smoke-test local (banco em memória)."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
