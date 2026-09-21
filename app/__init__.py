from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from app.config import Config
from app.errores import ErrorAPI


API_VERSION = "v1"

db = SQLAlchemy()
migrate = Migrate()


def create_app(configuracion_pruebas=None):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    if configuracion_pruebas:
        app.config.update(configuracion_pruebas)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"])

    # Importación diferida para evitar dependencias circulares.
    from app.dominios.usuarios.controladores import admin_bp, usuarios_bp

    app.register_blueprint(
        usuarios_bp,
        url_prefix="/api/v1/usuarios",
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/v1/admin",
    )

    @app.errorhandler(ValidationError)
    def manejar_error_validacion(error):
        return {
            "error": "datos_invalidos",
            "mensaje": "Los datos enviados no son válidos.",
            "detalles": error.messages,
        }, 400

    @app.errorhandler(ErrorAPI)
    def manejar_error_api(error):
        return {
            "error": error.codigo or "error_api",
            "mensaje": error.mensaje,
        }, error.status_code

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "alojamientos-api",
            "version": API_VERSION,
        }, 200

    return app