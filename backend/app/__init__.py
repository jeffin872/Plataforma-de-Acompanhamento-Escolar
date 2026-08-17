from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt, cors
from app.utils.responses import erro


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # --- Extensões ---
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"]}})

    @jwt.unauthorized_loader
    def token_ausente(_motivo):
        return erro("Faça login para acessar este recurso.", status=401)

    @jwt.invalid_token_loader
    def token_invalido(_motivo):
        return erro("Sessão inválida. Faça login novamente.", status=401)

    @jwt.expired_token_loader
    def token_expirado(_header, _payload):
        return erro("Sua sessão expirou. Faça login novamente.", status=401)

    # Garante que todos os models sejam conhecidos pelo SQLAlchemy/Migrate.
    with app.app_context():
        from app import models  # noqa: F401

    # --- Blueprints (um por módulo do sistema) ---
    from app.auth.routes import auth_bp
    from app.admin.routes import admin_bp
    from app.academic.routes import academic_bp
    from app.responsavel.routes import responsavel_bp
    from app.documents.routes import documents_bp
    from app.fluxo_faltas.routes import (
        professor_faltas_bp,
        documentos_atestados_bp,
        admin_atestados_bp,
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(academic_bp)
    app.register_blueprint(responsavel_bp)
    app.register_blueprint(documents_bp)

    # Fluxo "Gestão de Faltas e Atestados" — MVP com armazenamento em
    # memória (ver app/fluxo_faltas/store.py), independente do fluxo real
    # de Falta/Documento acima, que continua gravando no PostgreSQL.
    app.register_blueprint(professor_faltas_bp)
    app.register_blueprint(documentos_atestados_bp)
    app.register_blueprint(admin_atestados_bp)

    @app.get("/api/saude")
    def saude():
        """Endpoint simples para checar se a API está no ar."""
        return {"status": "ok", "servico": "Plataforma de Acompanhamento Escolar"}

    # --- Handlers de erro padronizados (mesmo formato do resto da API) ---
    @app.errorhandler(404)
    def nao_encontrado(_e):
        return erro("Recurso não encontrado.", status=404)

    @app.errorhandler(405)
    def metodo_nao_permitido(_e):
        return erro("Método não permitido para esta rota.", status=405)

    @app.errorhandler(500)
    def erro_interno(_e):
        app.logger.exception("Erro interno não tratado")
        return erro("Erro interno do servidor.", status=500)

    return app
