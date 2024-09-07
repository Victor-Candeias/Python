# flask_restful_api/app/websocket_routes.py

from flask import request, Blueprint
from flask_sock import Sock
from websocket_manager.websocket_manager import WebSocketManager

# Create a Blueprint for WebSocket routes
ws_bp = Blueprint('ws_bp', __name__)
sock = Sock()

# Initialize the WebSocket Manager
ws_manager = WebSocketManager()

# Handle WebSocket connections
@sock.route('/ws')
def websocket_handler(ws):
    client_id = request.remote_addr  # Alternatively, use a custom ID
    filters = request.args.to_dict()  # Retrieve any filters passed as query params
    ws_manager.add_client(client_id, ws, filters)

    try:
        while True:
            # Wait to receive a message from the client
            message = ws.receive()
            if message is None:
                break  # Client has disconnected
            # Handle received message (e.g., broadcasting, processing)
            ws_manager.send_message_to_client(client_id, message)
    finally:
        # Ensure the client is removed when the connection is closed
        ws_manager.remove_client(client_id)

# Example HTTP route to send a message to a group
@ws_bp.route('/send_group_message', methods=['POST'])
def send_group_message():
    filter_key = request.json.get('filter_key')
    message = request.json.get('message')
    ws_manager.send_message_to_group(filter_key, message)
    return {"status": "Message sent to group"}, 200

def init_app(app):
    sock.init_app(app)  # Initialize Flask-Sock with the Flask app
    app.register_blueprint(ws_bp)
