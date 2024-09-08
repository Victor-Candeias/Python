# run.py

# flask_restful_api/run.py
from flask import Flask
from flask_socketio import SocketIO
from app.websocket_events import init_events  # Import init_events function
from app import create_app

# Initialize Flask app
app = create_app()

socketio = SocketIO(app, cors_allowed_origins="*")  # Handle CORS for local development

# Initialize SocketIO and register events/routes
init_events(app, socketio)

# Load configuration from config.py
# Set the environment by choosing the config class to use
app.config.from_object('config.DevelopmentConfig')  # For development, use DevelopmentConfig

if __name__ == '__main__':
    # socketio.run(app, host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
    socketio.run(app, host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])

# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
