import serial
import time
import logging
from typing import Callable, Optional

class SerialConnectionManager:
    def __init__(self, port: str, baud_rate: int = 9600, byte_size: int = 8, parity: str = "N", stop_bits: float = 1, timeout: float = 1.0,
                 xon_xoff: bool = False, rtscts: bool = False,
                 max_retries: int = 5, retry_delay: float = 5.0, 
                 exponential_backoff: bool = False, on_data_received: Optional[Callable[[str], None]] = None, on_reconnect: Optional[Callable] = None):
        self.port = port
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.parity = parity
        self.timeout = timeout
        self.stop_bits = stop_bits
        self.xon_xoff = xon_xoff
        self.rtscts = rtscts
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.exponential_backoff = exponential_backoff
        self.serial_connection: Optional[serial.Serial] = None
        self._running = False
        self.on_data_received = on_data_received
        self.on_reconnect = on_reconnect

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """Tenta estabelecer uma conexão com a porta serial."""
        retries = 0
        delay = self.retry_delay
        while retries < self.max_retries:
            try:
                self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
                self.logger.info(f"Conexão serial estabelecida em {self.port} com baud rate {self.baud_rate}.")
                return True
            except serial.SerialException as e:
                retries += 1
                self.logger.error(f"Erro ao conectar: {e} (tentativa {retries}/{self.max_retries})")
                if self.exponential_backoff:
                    delay *= 2
                self.logger.info(f"Tentando reconectar em {delay} segundos...")
                time.sleep(delay)
        self.logger.error("Falha ao conectar após várias tentativas.")
        return False

    def disconnect(self):
        """Fecha a conexão com a porta serial."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.logger.info("Conexão serial fechada.")
        self._running = False

    def reconnect(self):
        """Tenta reconectar à porta serial."""
        self.disconnect()
        if self.connect() and self.on_reconnect:
            self.on_reconnect()

    def send_data(self, data: str):
        """Envia dados através da porta serial."""
        if not self.serial_connection or not self.serial_connection.is_open:
            self.logger.error("Tentativa de envio falhou: conexão serial não está aberta.")
            return False
        try:
            self.serial_connection.write(data.encode('utf-8'))
            self.logger.info(f"Dados enviados: {data}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Erro ao enviar dados: {e}")
            return False

    def receive_data(self) -> Optional[str]:
        """Recebe dados da porta serial."""
        if not self.serial_connection or not self.serial_connection.is_open:
            self.logger.error("Tentativa de leitura falhou: conexão serial não está aberta.")
            return None
        try:
            if self.serial_connection.in_waiting > 0:
                data = self.serial_connection.readline().decode('utf-8').strip()
                self.logger.info(f"Dados recebidos: {data}")
                if self.on_data_received:
                    self.on_data_received(data)
                return data
            return None
        except serial.SerialException as e:
            self.logger.error(f"Erro ao receber dados: {e}")
            return None

    def start_communication(self):
        """Inicia o processo de comunicação, incluindo reconexão automática se necessário."""
        self._running = True
        if not self.connect():
            self._running = False
            return
        
        self.logger.info("Comunicação iniciada.")
        while self._running:
            # Implementar a lógica de comunicação contínua aqui, se necessário.
            self.receive_data()
            time.sleep(1)

    def stop_communication(self):
        """Para a comunicação e fecha a conexão."""
        self.logger.info("Parando a comunicação.")
        self._running = False
        self.disconnect()
