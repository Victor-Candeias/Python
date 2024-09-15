# /app/websocket_events.py

import logging
from flask_socketio import emit, send
from controller.websocket_manager.websocket_manager import WebSocketManager
from messages import Messages

def init_events(app, socketio):
    """
    Initializes the routes and WebSocket events.

    Args:
        app (Flask): Flask app instance.
        socketio (SocketIO): Flask-SocketIO instance.
    """
    logger = logging.getLogger(__name__)

    # Initialize WebSocketManager
    ws_manager = WebSocketManager(socketio)

    @socketio.on('connect')
    def handle_connect():
        """
        WebSocket event: client connect.
        """
        logger.info("Client connected")
        send({ "message":"Client connected!", "status": Messages._instance.STATUS_RESULT_OK })

    @socketio.on('disconnect')
    def handle_disconnect():
        """
        WebSocket event: client disconnect.
        """
        logger.info({ "message":"Client disconnected!", "status": Messages._instance.STATUS_RESULT_OK })

    @socketio.on('message')
    def handle_message(data):
        """
        WebSocket event: handle incoming messages from clients.

        Args:
            data (str): Message data from the client.
        """
        logger.info(f"Received message: {data}")
        # ws_manager.send_message(data)

    @socketio.on('join')
    def handle_join(data):
        """
        WebSocket event: add client to rooms.

        Args:
            data (dict): Contains list of rooms to join.
        """
        rooms = data.get('rooms', [])
        if rooms:
            try:
                ws_manager.join_rooms(rooms)
                logger.info(f"Client joined rooms: {', '.join(rooms)}")
            except Exception as e:
                logger.error(f"Error joining rooms: {e}")
                emit('error', {'message': f'Failed to join rooms: {e}'})

    @socketio.on('leave')
    def handle_leave(data):
        """
        WebSocket event: remove client from rooms.

        Args:
            data (dict): Contains list of rooms to leave.
        """
        rooms = data.get('rooms', [])
        if rooms:
            try:
                ws_manager.leave_rooms(rooms)
                logger.info(f"Client left rooms: {', '.join(rooms)}")
            except Exception as e:
                logger.error(f"Error leaving rooms: {e}")
                emit('error', {'message': f'Failed to leave rooms: {e}'})

    @socketio.on('room_message')
    def handle_room_message(data):
        """
        WebSocket event: handle room-specific messages.

        Args:
            data (dict): Contains list of rooms and message.
        """
        rooms = data.get('rooms', [])
        message = data.get('message')

        if rooms and message:
            ws_manager.send_message(message, rooms)
