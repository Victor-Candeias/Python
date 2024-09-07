# flask_restful_api/websocket_manager/websocket_manager.py

from collections import defaultdict
from .client import WebSocketClient

class WebSocketManager:
    def __init__(self, host='localhost', port=5000):
        self.clients = {}
        self.client_groups = defaultdict(list)
        self.host = host
        self.port = port

    def add_client(self, client_id, connection, filters=None):
        # Adiciona o cliente
        client = WebSocketClient(client_id, connection, filters)
        self.clients[client_id] = client

        # Organiza o cliente nos grupos, conforme os filtros
        for key, value in filters.items():
            self.client_groups[key].append(client)
        
        # Constrói a URI do WebSocket
        uri = f"ws://{self.host}:{self.port}/ws/{client_id}"
        
        # Retorna a URI
        return uri

    def remove_client(self, client_id):
        client = self.clients.pop(client_id, None)
        if client:
            client.close_connection()
            for key in client.filters.keys():
                self.client_groups[key].remove(client)

    def send_message_to_client(self, client_id, message):
        client = self.clients.get(client_id)
        if client:
            client.send_message(message)

    def send_message_to_group(self, filter_key, message):
        clients = self.client_groups.get(filter_key, [])
        for client in clients:
            client.send_message(message)

    def close_all_connections(self):
        for client_id, client in list(self.clients.items()):
            self.remove_client(client_id)
