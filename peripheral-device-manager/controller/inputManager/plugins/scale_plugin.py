# controller/plugins/scale_plugin.py
import json
import os
import threading
import time
from config import Config
from controller.plugin_base import PluginBase
from messages import Messages
from controller.utilities import Utilities, OPERATING_SYSTEM_TYPE
from controller.serialPortManager.linux_serial_connection_manager import LinuxSerialPortManager
from controller.serialPortManager.windows_serial_port_manager import WindowsAsyncSerialManager

# set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class ScalePlugin(PluginBase):
    def __init__(self):
        """
        initialize the Scale plugin class by calling the base class initializer.
        """
        super().__init__(os.path.join(os.path.dirname(__file__)))
        
    def start(self):
        """
        starts reading the scale.
        """
        if (self.jsonConfigurationPlugin != ''):
            self._running = True
            self._thread = threading.Thread(target=self._read_from_serial)
            self._thread.start()

    def stop(self):
        """
        stop read the scale.
        """
        self._running = False
        if self._thread.is_alive():
            self._thread.join()
        
        if (Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX):
            if self.linux_serial_port_manager.serial_connection and self.linux_serial_port_manager.serial_connection.is_open:
                self.linux_serial_port_manager.stop_communication()
                self.linux_serial_port_manager.serial_connection.close()
        else:
            self.windows_serial_port_manager.close_port()
            
        self.logger.info("Serial connection closed.")
            
    def _read_from_serial(self):
        """
        process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"Processing {self.plugin_name}")

        # connect to serial port
        result_connect = False
        
        from controller.utilities import Utilities, OPERATING_SYSTEM_TYPE
                
        if Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX:
            # Initialize the linux serial port manager
            self.linux_serial_port_manager = LinuxSerialPortManager(
                                                    self.jsonConfigurationPlugin['port'], 
                                                    self.jsonConfigurationPlugin['baud_rate'], 
                                                    self.jsonConfigurationPlugin['byte_size'],
                                                    self.jsonConfigurationPlugin['parity'],
                                                    self.jsonConfigurationPlugin['stop_bits'])
        else:
            self.windows_serial_port_manager = WindowsAsyncSerialManager(self.jsonConfigurationPlugin['port'])
            
        if (Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX):
            result_connect = self.linux_serial_port_manager.connect()
            self.linux_serial_port_manager.start_communication()
        else:
            result_connect = self.windows_serial_port_manager.open_port()
           
        status_result = "200"

        if result_connect:
            # if connected, send the data
            try:
                self._running = True

                # internal method to continuously read data from the serial port and reconnect in case of failure.
                while self._running:
                    if (Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX):
                        if not self.linux_serial_port_manager.serial_connection or not self.linux_serial_port_manager.serial_connection.is_open:
                            if not self.linux_serial_port_manager.connect():
                                self._running = False
                                return
                    else:
                        if not self.windows_serial_port_manager.check_serial_connection():
                            if not self.windows_serial_port_manager.open_port():
                                self._running = False
                                return
                    try:
                        data = ""
                        
                        if (Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX):
                            if self.linux_serial_port_manager.serial_connection.in_waiting > 0:
                                data = self.linux_serial_port_manager.serial_connection.readline().decode('utf-8').strip()
                                # self._latest_value = self._process_data(data)
                                # self.logger.debug(f"Data read from the scale: {data}")
                        else:
                            data = self.windows_serial_port_manager.listen_for_data()

                        self.logger.debug(f"Data read from the barcode: {data}")
                        
                    except UnicodeDecodeError as e:
                        self.logger.error(f"Error in decoding data: {e}")

                    time.sleep(0.1)

            except:
                self.logger.info(f"Processing {self.plugin_name} result {status_result}")
        else:
            # connection failed
            status_result = "400"

        self.logger.info(f"Processing {self.plugin_name} result {status_result}")

        self.linux_serial_port_manager = None
        self.windows_serial_port_manager = None
        
        return status_result

    def _process_data(self, data: str):
        """
        processes data received from the scale.
        """
        try:
            # call websocket
            # call websocket
            from controller.utilities import Utilities
        
            resultStatus = Messages._instance.STATUS_RESULT_OK
        
            try:
                serverUrl = Config._instance.PROTOCOL + Config._instance.HOST + ":" + Config._instance.PORT
                
                Utilities.sendDataToClients(serverUrl, sessionId=None, inputType=PluginBase.plugin_name, message=data)
            except:
                resultStatus = Messages._instance.STATUS_RESULT_ERROR

            # return result
            return jsonify({'status': 'success', 'message': 'Input data sent to WebSocket clients'}), resultStatus
        
        except ValueError:
            self.logger.warning(f"Invalid data received: {data}")
            return None

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, ScalePlugin())
