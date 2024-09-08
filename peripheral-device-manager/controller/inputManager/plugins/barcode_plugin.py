# controller/plugins/label_plugin.py
import os
import threading
import time
from controller.plugin_base import PluginBase

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class BarcodePlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Barcode plugin class by calling the base class initializer.
        """
        super().__init__(os.path.join(os.path.dirname(__file__)))

    def start(self):
        """Inicia a leitura da balança."""
        self._running = True
        self._thread = threading.Thread(target=self._read_from_serial)
        self._thread.start()

    def stop(self):
        """Para a leitura da balança."""
        self._running = False
        if self._thread.is_alive():
            self._thread.join()
        if self.serial_port_manager.serial_connection and self.serial_port_manager.serial_connection.is_open:
            self.serial_port_manager.stop_communication()
            self.serial_port_manager.serial_connection.close()
            self.logger.info("Conexão serial fechada.")

    def _read_from_serial(self):
        """
        Process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"Processing {self.plugin_name}")

        # Connect to serial port
        result_connect = self.serial_port_manager.connect()
        status_result = "200"

        if result_connect:
            # If connected, send the data
            try:
                self.serial_port_manager.start_communication()

                self._running = True

                """Método interno para ler continuamente os dados da porta serial e reconectar em caso de falha."""
                while self._running:
                    if not self.serial_connection or not self.serial_connection.is_open:
                        if not self._connect_serial():
                            self._running = False
                            return

                    try:
                        if self.serial_port_manager.serial_connection.in_waiting > 0:
                            data = self.serial_port_manager.serial_connection.readline().decode('utf-8').strip()
                            self._latest_value = self._process_data(data)
                            self.logger.debug(f"Dado lido da balança: {data}")

                    except UnicodeDecodeError as e:
                        self.logger.error(f"Erro na decodificação dos dados: {e}")

                    time.sleep(0.1)

            except:
                self.logger.info(f"Processing {self.plugin_name} result {status_result}")
        else:
            # Connection failed
            status_result = "400"

        self.logger.info(f"Processing {self.plugin_name} result {status_result}")
        return status_result

    def _process_data(self, data: str):
        """Processa os dados recebidos da balança."""
        try:
            # call websockect

            return data
        
        except ValueError:
            self.logger.warning(f"Dado inválido recebido: {data}")
            return None

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, BarcodePlugin())
