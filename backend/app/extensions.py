"""
Instâncias das extensões Flask.

Ficam separadas em um módulo próprio para evitar import circular entre
app/__init__.py e os arquivos de models/rotas (todos importam daqui).
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
