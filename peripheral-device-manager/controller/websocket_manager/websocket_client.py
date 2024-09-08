import logging
import time
import socketio

class WebSocketClient:
    def __init__(self, server_url):
        # Initialize the Socket.IO client
        self.logger = logging.getLogger(__name__)
        self.sio = socketio.Client()
        self.server_url = server_url
        self.running = True

        # Define event handlers
        @self.sio.event
        def connect():
            self.logger.info(f"connect():Connected to the server")

            # Emit a message to join rooms if needed
            if hasattr(self, 'session_id') and hasattr(self, 'filters'):
                self.sio.emit('join', {'sessionId': self.session_id, 'filters': self.filters})

            elif hasattr(self, 'session_id') == False and hasattr(self, 'filters'):
                self.sio.emit('join', {'filters': self.filters})

            elif hasattr(self, 'session_id') and hasattr(self, 'filters') == False:
                self.sio.emit('join', {'sessionId': self.session_id})

            # Optionally send a message after connecting
            self.sio.emit('message', 'Hello, server!')

        @self.sio.event
        def disconnect():
            print('Disconnected from the server')

        @self.sio.event
        def messageData(data):
            print('Received message:', data)

    def connect(self, session_id, filters):
        self.session_id = session_id
        self.filters = filters
        # Connect to the WebSocket server
        self.sio.connect(self.server_url)

    def disconnect(self):
        # Disconnect from the WebSocket server
        self.sio.disconnect()

    def send_message(self, message):
        # Send a message to the server
        self.sio.emit('message', message)

    def keep_running(self):
        # Keep the program running to listen for events
        while self.running:
            time.sleep(1)