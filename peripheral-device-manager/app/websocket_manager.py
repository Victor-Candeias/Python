# app/websocket_manager.py
from flask_sock import Sock

class WebSocketManager:
    def __init__(self):
        # Armazena todas as conexões WebSocket. Cada cliente pode ter várias conexões.
        self.clients = {}

    def register_client(self, client_id):
        """Registra um cliente para o WebSocket, preparando para a comunicação"""
        if client_id not in self.clients:
            self.clients[client_id] = {
                'connections': [],  # Lista para armazenar várias conexões WebSocket
                'filters': set(),
            }

    def set_filters(self, client_id, filters):
        """Define filtros para um cliente específico"""
        if client_id in self.clients:
            self.clients[client_id]['filters'] = set(filters)

    def associate_websocket(self, client_id, ws):
        """Associa uma nova conexão WebSocket com o cliente"""
        if client_id in self.clients:
            self.clients[client_id]['connections'].append(ws)

    def send_message(self, client_id, message_type, message_data):
        """Envia uma mensagem para um cliente específico via WebSocket"""
        if client_id in self.clients:
            for ws in self.clients[client_id]['connections']:
                try:
                    ws.send(f"{message_type}: {message_data}")
                except Exception as e:
                    print(f"Failed to send message to client {client_id}: {e}")

    def broadcast_message(self, message_type, message_data):
        """Envia uma mensagem para todos os clientes conectados"""
        for client_id, client_info in self.clients.items():
            for ws in client_info['connections']:
                try:
                    ws.send(f"{message_type}: {message_data}")
                except Exception as e:
                    print(f"Failed to send broadcast message to client {client_id}: {e}")

    def remove_client(self, client_id):
        """Remove todas as conexões WebSocket de um cliente específico"""
        if client_id in self.clients:
            for ws in self.clients[client_id]['connections']:
                try:
                    ws.close()
                except Exception as e:
                    print(f"Error closing connection for client {client_id}: {e}")
            del self.clients[client_id]

    def remove_connection(self, client_id, ws):
        """Remove uma conexão WebSocket específica para um cliente"""
        if client_id in self.clients:
            try:
                ws.close()
                self.clients[client_id]['connections'].remove(ws)
            except Exception as e:
                print(f"Error removing connection for client {client_id}: {e}")
            if not self.clients[client_id]['connections']:
                del self.clients[client_id]

ws_manager = WebSocketManager()
