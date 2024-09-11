# /controller/websocket_manager.py

from flask_socketio import SocketIO, join_room, leave_room

class WebSocketManager:
    def __init__(self, socketio: SocketIO):
        """
        Initializes the WebSocketManager with a SocketIO instance, which will handle all WebSocket communication.

        Args:
            socketio (SocketIO): SocketIO lib instance
        """
        self.socketio = socketio

    def send_message(self, message: str, rooms: list = None):
        """
        Sends a message to one or more specific rooms. If no rooms are provided, it emits the message to all clients.

        Args:
            message (str): The message to send.
            rooms (list, optional): A list of room names where the message should be sent.. Defaults to None.
        """
        if rooms:
            for room in rooms:
                self.socketio.emit('message', message, room=room)
        else:
            self.socketio.emit('message', message)

    def join_rooms(self, rooms: list):
        """
        Makes the current user join multiple rooms and notifies them upon joining.

        Args:
            rooms (list): A list of room names the user should join.
            
        Flow:
            The join_room() function adds the user to the specified room(s).
            A confirmation message is sent to each room after joining.
        """
        for room in rooms:
            join_room(room)
            self.send_message(f"You have joined the room: {room}", [room])

    def leave_rooms(self, rooms: list):
        """
        Makes the current user leave multiple rooms and notifies them upon leaving.

        Args:
            rooms (list): A list of room names the user should leave.
            
            Flow:
                The leave_room() function removes the user from the specified room(s).
                A message is sent to each room after leaving.
        """
        for room in rooms:
            leave_room(room)
            self.send_message(f"You have left the room: {room}", [room])

    def broadcast_message(self, message: str):
        """
        Sends a message to all connected WebSocket clients.

        Args:
            message (str): The message to send.
        """
        self.socketio.emit('message', message, broadcast=True)
