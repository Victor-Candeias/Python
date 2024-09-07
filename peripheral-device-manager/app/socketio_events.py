# flask_restful_api/app/socketio_events.py

from flask import request, Blueprint
from flask_socketio import SocketIO
from controller.websocket_manager.websocket_manager import WebSocketManager

# Create a Blueprint for HTTP routes
socketio_bp = Blueprint('socketio_bp', __name__)

# Initialize the WebSocket Manager
ws_manager = WebSocketManager()

# Create a SocketIO instance (we'll pass the Flask app to it later)
socketio = SocketIO()

# WebSocket connection event
@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    filters = request.args.to_dict()
    ws_manager.add_client(client_id, request.namespace, filters)

# WebSocket disconnection event
@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    ws_manager.remove_client(client_id)

# WebSocket message event
@socketio.on('send_message')
def handle_message(data):
    client_id = request.sid
    message = data.get('message', '')
    ws_manager.send_message_to_client(client_id, message)

# HTTP route to send a message to a group
@socketio_bp.route('/send_group_message', methods=['POST'])
def send_group_message():
    filter_key = request.json.get('filter_key')
    message = request.json.get('message')
    ws_manager.send_message_to_group(filter_key, message)
    return {"status": "Message sent to group"}, 200

def init_socketio(app):
    # Initialize the Flask-SocketIO with the Flask app
    socketio.init_app(app)

    # Register the Blueprint for HTTP routes
    app.register_blueprint(socketio_bp)
