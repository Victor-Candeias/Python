# /ws_manager.py

from flask_socketio import SocketIO, join_room, leave_room

class WebSocketManager:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio

    def send_message(self, message: str, rooms: list = None):
        """Send a message to specific rooms"""
        if rooms:
            for room in rooms:
                self.socketio.emit('message', message, room=room)
        else:
            self.socketio.emit('message', message)

    def join_rooms(self, rooms: list):
        """Join multiple rooms"""
        for room in rooms:
            join_room(room)
            self.send_message(f"You have joined the room: {room}", [room])

    def leave_rooms(self, rooms: list):
        """Leave multiple rooms"""
        for room in rooms:
            leave_room(room)
            self.send_message(f"You have left the room: {room}", [room])

    def broadcast_message(self, message: str):
        """Broadcast a message to all connected clients"""
        self.socketio.emit('message', message, broadcast=True)
