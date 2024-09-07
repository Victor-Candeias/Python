# flask_restful_api/websocket_manager/client.py

class WebSocketClient:
    def __init__(self, client_id, connection, filters=None):
        self.client_id = client_id
        self.connection = connection
        self.filters = filters or {}

    def send_message(self, message):
        self.connection.send(message)

    def close_connection(self):
        self.connection.close()
