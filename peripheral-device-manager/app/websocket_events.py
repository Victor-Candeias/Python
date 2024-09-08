# /events.py

from flask import render_template
from flask_socketio import send
from controller.websocket_manager.websocket_manager import WebSocketManager  # Import WebSocketManager

# Define a function to initialize the routes and WebSocket events
def init_events(app, socketio):
    # Initialize WebSocketManager
    ws_manager = WebSocketManager(socketio)

    # WebSocket event: client connect
    @socketio.on('connect')
    def handle_connect():
        print("Client connected")
        send("Welcome to the WebSocket!")

    # WebSocket event: client disconnect
    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected")

    # WebSocket event: handle message
    @socketio.on('message')
    def handle_message(data):
        print(f"Received message: {data}")

        if (data == 'Hello from the external client!'):
            return
    
        # Use WebSocketManager to echo the message
        ws_manager.send_message(f"Echo: {data}")

    @socketio.on('join')
    def handle_join(data):
        rooms = data.get('rooms', [])
        if rooms:
            ws_manager.join_rooms(rooms)
            for room in rooms:
                send(f"You have joined the room: {room}", room=room)

    @socketio.on('leave')
    def handle_leave(data):
        rooms = data.get('rooms', [])
        if rooms:
            ws_manager.leave_rooms(rooms)
            for room in rooms:
                send(f"You have left the room: {room}", room=room)
