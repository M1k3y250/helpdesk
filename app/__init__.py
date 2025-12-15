import os
from flask import Flask
from flask_mysqldb import MySQL
from .routes import bp as routes_bp
from config import Config

mysql = MySQL()

def create_app():
    # Base del proyecto (helpdesk/)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Carpetas fuera de app/
    template_dir = os.path.join(base_dir, "templates")
    static_dir = os.path.join(base_dir, "static")

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )

    # Configuración
    app.config.from_object(Config)

    # Inicializar MySQL
    mysql.init_app(app)

    # Registrar blueprint
    app.register_blueprint(routes_bp)

    return app
