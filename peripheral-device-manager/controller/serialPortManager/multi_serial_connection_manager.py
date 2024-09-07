from typing import List, Dict, Optional

from controller.serialPortManager.serial_connection_manager import SerialConnectionManager

class MultiSerialConnectionManager:
    def __init__(self):
        self.connections: Dict[str, SerialConnectionManager] = {}

    def add_connection(self, name: str, port: str, baud_rate: int = 9600, timeout: float = 1.0, max_retries: int = 5, retry_delay: float = 5.0, exponential_backoff: bool = False, on_data_received: Optional[Callable[[str], None]] = None, on_reconnect: Optional[Callable] = None):
        """Adiciona uma nova conexão serial ao gerenciador."""
        connection = SerialConnectionManager(
            port=port,
            baud_rate=baud_rate,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            exponential_backoff=exponential_backoff,
            on_data_received=on_data_received,
            on_reconnect=on_reconnect
        )
        self.connections[name] = connection
        self.connections[name].start_communication()

    def remove_connection(self, name: str):
        """Remove uma conexão e para a comunicação."""
        if name in self.connections:
            self.connections[name].stop_communication()
            del self.connections[name]

    def send_data(self, name: str, data: str):
        """Envia dados por uma conexão específica."""
        if name in self.connections:
            self.connections[name].send_data(data)

    def get_connection(self, name: str) -> Optional[SerialConnectionManager]:
        """Retorna uma instância de SerialConnectionManager específica."""
        return self.connections.get(name, None)

    def stop_all(self):
        """Para todas as comunicações e fecha todas as conexões."""
        for connection in self.connections.values():
            connection.stop_communication()
        self.connections.clear()
