# server/app/__init__.py
from flask import Flask
from flask_cors import CORS
from controllers import device_manager

def create_app():
    # app = Flask(__name__)
    app = Flask(__name__, template_folder='../templates', static_folder='assets')
    
    # Enable CORS for a specific origin
    CORS(app, resources={r"/*": {"origins": "*", "methods": "*", "allow_headers": ["Content-Type"]}})
    # CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS", "DELETE"], "allow_headers": ["Content-Type", "Authorization"]}})
    
    # Register the blueprint with the application
    from app.routes import api_dm  # Ensure this import works
    app.register_blueprint(api_dm)
    
    return app
