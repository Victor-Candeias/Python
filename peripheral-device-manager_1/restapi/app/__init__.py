from flask import Flask
from flask_cors import CORS
from .routes import init_routes

def create_app(config_filename=None):
    app = Flask(__name__)
    CORS(app)

    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_object('config')  # Default config

    # Initialize routes
    init_routes(app)

    return app
