# /websocket_events.py

import logging
from flask import render_template
from flask_socketio import send
from controller.websocket_manager.websocket_manager import WebSocketManager

def init_events(app, socketio):
    """
    define a function to initialize the routes and WebSocket events

    Args:
        app (class app): current app created
        socketio (class): websocket lib
    """
    
    # log manager
    logger = logging.getLogger(__name__,)
    
    # initialize WebSocketManager
    ws_manager = WebSocketManager(socketio)

    @socketio.on('connect')
    def handle_connect():
        """
        websocket event: client connect
        """
        logger.info("Client connected")
        send("Welcome to the WebSocket!")

    @socketio.on('disconnect')
    def handle_disconnect():
        """
        websocket event: client disconnect
        """
        logger.info("Client disconnected")

    @socketio.on('message')
    def handle_message(data):
        """
        websocket event: handle message

        Args:
            data (str): data to send to the client
        """
        logger.info(f"Received message: {data}")

        # Use websocketManager to echo the message
        ws_manager.send_message(f"Echo: {data}")

    @socketio.on('join')
    def handle_join(data):
        """
        add client to a room

        Args:
            data (str): rooms to add
        """
        rooms = data.get('rooms', [])
        if rooms:
            ws_manager.join_rooms(rooms)
            for room in rooms:
                logger.info(f"You have joined the room: {room}")

    @socketio.on('leave')
    def handle_leave(data):
        """
        remove client from room

        Args:
            data (str): rooms to remove
        """
        rooms = data.get('rooms', [])
        if rooms:
            ws_manager.leave_rooms(rooms)
            for room in rooms:
                logger.info(f"You have left the room: {room}")
