
from flask import Flask
from flask_cors import CORS
from app.logging_config import setup_logging

def create_app():
    """
    create_app _summary_

    Returns:
        _type_: _description_
    """
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS para todas as rotas

    # Registrar blueprints e outras configurações do app
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    # Additional setup can go here (e.g., database, logging)
    setup_logging()

    return app
