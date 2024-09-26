# /controller/websocket_manager/websocket_client.py

import logging
import time
import socketio

class WebSocketClient:
    def __init__(self, serverUrl):
        """
        Initializes the Socket.IO client.

        Args:
            serverUrl (str): WebSocket server URL.
        """
        self.logger = logging.getLogger(__name__)
        self.sio = socketio.Client()
        self.serverUrl = serverUrl
        self.running = False

        self.logger.info(f"websocket_client.py;__init__();self.serverUrl={self.serverUrl}")
        self.logger.info(f"websocket_client.py;__init__();self.running={self.running}")
        
        @self.sio.event
        def connect():
            """
            WebSocket event: connect to the WebSocket server.
            """
            self.logger.info(f"websocket_client.py;connect();Connected from the server")
            if hasattr(self, 'filters'):
                self.sio.emit('join', {'rooms': self.filters})

        @self.sio.event
        def disconnect():
            """
            WebSocket event: disconnect from the WebSocket server.
            """
            self.logger.info(f"websocket_client.py;disconnect();Disconnected from the server")

        @self.sio.event
        def messageData(data):
            """
            WebSocket event: handle incoming messages.

            Args:
                data (str): Message data received from the server.
            """
            self.logger.info(f"websocket_client.py;messageData();data={data}")

    def connect(self, filters=None, session_id=None):
        """
        Connect to the WebSocket server and join rooms.

        Args:
            filters (list): List of rooms to join.
            session_id (str): Optional session ID for the client.
        """
        self.filters = filters or []
        self.session_id = session_id
        self.sio.connect(self.serverUrl)
        self.running = True
        
        self.logger.info(f"websocket_client.py;connect();self.filters={self.filters}")
        self.logger.info(f"websocket_client.py;connect();self.session_id={self.session_id}")
        self.logger.info(f"websocket_client.py;connect();self.running={self.running}")
        
    def disconnect(self):
        """
        Disconnect from the WebSocket server.
        """
        self.running = False
        self.sio.disconnect()

    def send_message_to_rooms(self, rooms, message):
        """
        Send a message to multiple rooms on the server.

        Args:
            rooms (list[str]): List of rooms to send the message to.
            message (str): Message to send.
        """
        if rooms and message:
            self.logger.info(f"websocket_client.py;send_message_to_rooms();rooms={rooms}")
            self.logger.info(f"websocket_client.py;send_message_to_rooms();message={message}")
            
            self.sio.emit('room_message', {'rooms': rooms, 'message': message})

    def keep_running(self, waitTimeToExit=0):
        """
        Keep the program running to listen for WebSocket events.
        """
        self.logger.info(f"websocket_client.py;keep_running();waitTimeToExit={waitTimeToExit}")
        
        while self.running:
            if waitTimeToExit != 0:
                time.sleep(waitTimeToExit)
                break
            else:
                time.sleep(1)
