# /app/websocket_events.py

import logging
import json
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
        logger.info("websocket_events.py;onConnect();Client connected")
        
        send({ "message":"Client connected!", "status": Messages._instance.STATUS_RESULT_OK })

    @socketio.on('disconnect')
    def handle_disconnect():
        """
        WebSocket event: client disconnect.
        """
        logger.info("websocket_events.py;onDisconnect();Client disconnected")
        
    # @socketio.on('message')
    # def handle_message(data):
    #     """
    #     WebSocket event: handle incoming messages from clients.

    #     Args:
    #         data (str): Message data from the client.
    #     """
    #     logger.info(f"Received message: {data}")
    #     # ws_manager.send_message(data)

    @socketio.on('join')
    def handle_join(data):
        """
        WebSocket event: add client to rooms.

        Args:
            data (dict): Contains list of rooms to join.
        """
        logger.info("websocket_events.py;onJoin();data={data}")
        
        rooms = data.get('rooms', [])
        if rooms:
            try:
                ws_manager.join_rooms(rooms)
                logger.info(f"websocket_events.py;onJoin();rooms={', '.join(rooms)}")
                                
            except Exception as e:
                logger.info("websocket_events.py;onJoin();Error joining rooms={e}")
                emit('error', {'message': f'Failed to join rooms: {e}'})

    @socketio.on('leave')
    def handle_leave(data):
        """
        WebSocket event: remove client from rooms.

        Args:
            data (dict): Contains list of rooms to leave.
        """
        logger.info("websocket_events.py;onLeave();message={data}")
        
        rooms = data.get('rooms', [])
        
        if rooms:
            try:
                ws_manager.leave_rooms(rooms)
                logger.info(f"websocket_events.py;onLeave();Client joined rooms={', '.join(rooms)}")
                
            except Exception as e:
                logger.info("websocket_events.py;onLeave();Error joining rooms={e}")
                emit('error', {'message': f'Failed to leave rooms: {e}'})

    @socketio.on('room_message')
    def handle_room_message(data):
        """
        WebSocket event: handle room-specific messages.

        Args:
            data (dict): Contains list of rooms and message.
        """
        logger.info("websocket_events.py;room_message();message={data}")
        
        rooms = data.get('rooms', [])
        message = data.get('message')

        if rooms and message:
            ws_manager.send_message(message, rooms)