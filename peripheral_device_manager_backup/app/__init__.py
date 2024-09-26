from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates')
    
    # Register API blueprint
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Register the main blueprint (config routes)
    from app.ui_app import ui_app
    app.register_blueprint(ui_app, url_prefix='/')

    return app
