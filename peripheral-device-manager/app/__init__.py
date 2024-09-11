
from flask import Flask
from flask_cors import CORS
from app.logging_config import setup_logging
    
def create_app():
    """
    Initialize the application
    
        Returns:
            class: Return the app instance
    """
    
    # create Flash app
    app = Flask(__name__)
    
    # enable CORS for all routes
    CORS(app)  

    # register blueprints and other app settings
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    # additional setup can go here (e.g., database, logging)
    setup_logging()

    return app
