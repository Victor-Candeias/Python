# /controller/websocket_manager/websocket_manager.py

import logging
from flask_socketio import SocketIO, join_room, leave_room

class WebSocketManager:
    def __init__(self, socketio: SocketIO):
        """
        Initializes the WebSocketManager with a SocketIO instance.

        Args:
            socketio (SocketIO): SocketIO instance.
        """
        self.logger = logging.getLogger(__name__)
        self.socketio = socketio

    def send_message(self, message: str, rooms: list = None):
        """
        Sends a message to one or more specific rooms. If no rooms are provided, broadcasts to all.

        Args:
            message (str): The message to send.
            rooms (list, optional): A list of rooms where the message should be sent.
        """ 
        if rooms:
            for room in rooms:
                self.socketio.emit('message', {'room': room, 'message': message}, room=room)
        else:
            self.socketio.emit('message', message, broadcast=True)

    def join_rooms(self, rooms: list):
        """
        Add the current user to multiple rooms.

        Args:
            rooms (list): A list of room names the user should join.
        """
        for room in rooms:
            join_room(room)
        
        self.logger.info(f"Joined rooms: {', '.join(rooms)}", rooms)

    def leave_rooms(self, rooms: list):
        """
        Remove the current user from multiple rooms.

        Args:
            rooms (list): A list of room names the user should leave.
        """
        for room in rooms:
            leave_room(room)
            
        self.logger.info(f"Left rooms: {', '.join(rooms)}", rooms)

    def broadcast_message(self, message: str, rooms: list = None):
        """
        Broadcasts a message to all clients or specific rooms.

        Args:
            message (str): The message to broadcast.
            rooms (list, optional): A list of rooms to target. Broadcasts to all if not provided.
        """
        if rooms:
            for room in rooms:
                self.socketio.emit('message', message, room=room)
        else:
            self.socketio.emit('message', message, broadcast=True)
