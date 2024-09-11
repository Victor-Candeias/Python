# flask_restful_api/run.py
from flask import Flask
from flask_socketio import SocketIO
from app.websocket_events import init_events
from app import create_app
from config import Config

# initialize Flask app
app = create_app()

# handle CORS for local development
socketio = SocketIO(app, cors_allowed_origins="*")  

# initialize SocketIO and register events/routes
init_events(app, socketio)

if __name__ == '__main__':
    socketio.run(app, host=Config._instance.HOST, port=Config._instance.PORT, debug=Config._instance.DEBUG)