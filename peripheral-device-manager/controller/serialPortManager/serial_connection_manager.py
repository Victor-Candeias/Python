import serial
import time
import logging
from typing import Callable, Optional

class SerialConnectionManager:
    def __init__(self, port: str, baud_rate: int = 9600, byte_size: int = 8, parity: str = "N", stop_bits: float = 1, timeout: float = 1.0,
                 xon_xoff: bool = False, rtscts: bool = False,
                 max_retries: int = 2, retry_delay: float = 3.0, 
                 exponential_backoff: bool = False, on_data_received: Optional[Callable[[str], None]] = None, on_reconnect: Optional[Callable] = None):
        """
        Initialize the Serial Port Manager

        Args:
            port (str): Port to connect
            baud_rate (int, optional): Port baud_rate. Defaults to 9600.
            byte_size (int, optional): Port byte_size. Defaults to 8.
            parity (str, optional): Port parity. Defaults to "N".
            stop_bits (float, optional): Port stop_bits. Defaults to 1.
            timeout (float, optional): Timeout of the connection attempt. Defaults to 1.0.
            xon_xoff (bool, optional): Port xon_xoff. Defaults to False.
            rtscts (bool, optional): Port rtscts. Defaults to False.
            max_retries (int, optional): Max. connection retries. Defaults to 5.
            retry_delay (float, optional): Delay time between connection attempts. Defaults to 5.0.
            exponential_backoff (bool, optional): indicates if the connection attempt has a delay time. Defaults to False.
            on_data_received (Optional[Callable[[str], None]], optional): Callback for receiving data. Defaults to None.
            on_reconnect (Optional[Callable], optional): Callback on reconnection. Defaults to None.
        """
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
        """
        Try to establish the connection to the Serial Port.

        Returns:
            bool: Indicates if the connection was made or not
        """
        
        retries = 0
        delay = self.retry_delay
        while retries < self.max_retries:
            try:
                self.serial_connection = serial.Serial(port=self.port, baudrate=self.baud_rate,bytesize=self.byte_size,parity=self.parity, stopbits=self.stop_bits, timeout=self.timeout)
                self.logger.info(f"Connection to serial stablish for port {self.port}.")
                return True
            except serial.SerialException as e:
                retries += 1
                self.logger.error(f"Connection error: {e} (Attempt {retries}/{self.max_retries})")
                if self.exponential_backoff:
                    delay *= 2
                self.logger.info(f"Try to reconnect in {delay} segundos...")
                time.sleep(delay)
                
        self.logger.error("Failed to connect after multiple attempts.")
        return False

    def disconnect(self):
        """
        Closes the connection to the serial port.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.logger.info("Connection to serial close.")
        self._running = False

    def reconnect(self):
        """
        Try reconnecting to the serial port.
        """
        self.disconnect()
        if self.connect() and self.on_reconnect:
            self.on_reconnect()

    def send_data(self, data: str):
        """
        Sends data through the serial port.

        Args:
            data (str): Data to send

        Returns:
            bool: True is ok. False on error.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            self.logger.error("Send attempt failed: serial connection is not open.")
            return False
        try:
            self.serial_connection.write(data.encode('utf-8'))
            self.logger.info(f"Data sent: {data}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Error sending data: {e}")
            return False

    def receive_data(self) -> Optional[str]:
        """
        Receives data from the serial port.

        Returns:
            Optional[str]: Return the received data
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            self.logger.error("Read attempt failed: serial connection is not open.")
            return None
        try:
            if self.serial_connection.in_waiting > 0:
                data = self.serial_connection.readline().decode('utf-8').strip()
                self.logger.info(f"Data receive: {data}")
                if self.on_data_received:
                    self.on_data_received(data)
                return data
            return None
        except serial.SerialException as e:
            self.logger.error(f"Error on receive data: {e}")
            return None

    def start_communication(self):
        """
        Starts the communication process, including automatic reconnection if necessary.
        """
        self._running = True
        if not self.connect():
            self._running = False
            return
        
        self.logger.info("Communication started.")
        while self._running:
            # TODO: Implement continuous communication logic here if necessary.
            self.receive_data()
            time.sleep(1)

    def stop_communication(self):
        """
        Stops communication and closes the connection.
        """
        self.logger.info("Stopping communication.")
        self._running = False
        self.disconnect()
