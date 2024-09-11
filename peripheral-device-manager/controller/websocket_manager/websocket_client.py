import logging
import time
import socketio

class WebSocketClient:
    def __init__(self, serverUrl):
        """
        Initialize the Socket.IO client

        Args:
            serverUrl (str): websocket server URL
        """
        self.logger = logging.getLogger(__name__)
        self.sio = socketio.Client()
        self.serverUrl = serverUrl
        self.running = False

        # Define event handlers
        @self.sio.event
        def connect():
            """
            Connect to the Websocket server
            """
            self.logger.info(f"connect():Connected to the server")

            # Emit a message to join rooms if needed
            if hasattr(self, 'sessionId') and hasattr(self, 'filters'):
                self.sio.emit('join', {'sessionId': self.sessionId, 'filters': self.filters})

            elif hasattr(self, 'sessionId') == False and hasattr(self, 'filters'):
                self.sio.emit('join', {'filters': self.filters})

            elif hasattr(self, 'sessionId') and hasattr(self, 'filters') == False:
                self.sio.emit('join', {'sessionId': self.sessionId})

            # Optionally send a message after connecting
            self.sio.emit('message', 'Hello, server!')

        @self.sio.event
        def disconnect():
            """
            Disconnect from websocket server
            """
            self.logger.info('Disconnected from the server')

        @self.sio.event
        def messageData(data):
            """
            Send message to the clients

            Args:
                data (str): message to send
            """
            self.logger.info("Received message:{data}")

    def connect(self, sessionId, filters):
        """
        Connect to the websocket server

        Args:
            sessionId (str): Connection sessionId from the client
            filters (array[str]): Filters to apply to the connection
        """
        self.sessionId = sessionId
        self.filters = filters
        
        # Connect to the WebSocket server
        self.sio.connect(self.serverUrl)

        self.running = True
        
    def disconnect(self):
        """
        Disconnect from the WebSocket server
        """
        self.running = False
        self.sio.disconnect()

    def send_message(self, message):
        """
        Send a message to the server

        Args:
            message (str): Message to send
        """
        self.sio.emit('message', message)

    def keep_running(self, waitTimeToExit = 0):
        """
        Keep the program running to listen for events
        """
        while self.running:
            if (waitTimeToExit != 0):
                time.sleep(waitTimeToExit)
                break
            else:
                time.sleep(1)