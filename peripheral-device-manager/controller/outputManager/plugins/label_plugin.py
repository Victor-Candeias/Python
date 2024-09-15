# controller/plugins/label_plugin.py
import asyncio
import base64
import binascii
import json
import os
import time
from controller.plugin_base import PluginBase
from controller.utilities import Utilities, OPERATING_SYSTEM_TYPE
from controller.serialPortManager.linux_serial_connection_manager import LinuxSerialPortManager
from controller.serialPortManager.windows_serial_port_manager import WindowsAsyncSerialManager

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class LabelPlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Label plugin class by calling the base class initializer.
        """
        super().__init__(os.path.join(os.path.dirname(__file__)))
        self._running = False

    def process(self, job):
        """
        Process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"Processing {self.plugin_name} Job {job['jobId']}")

        if (self.jsonConfigurationPlugin == ''):
            self.logger.info(f"Missing configuration for {self.plugin_name} for Job {job['jobId']}")
            return
        
        # initialize ok
        status_result = "200"
        
        # Connect to serial port
        result_connect = False
        
        from controller.utilities import Utilities, OPERATING_SYSTEM_TYPE
                
        # if Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX:
            # Initialize the linux serial port manager
        #     self.linux_serial_port_manager = LinuxSerialPortManager(
        #                                             self.jsonConfigurationPlugin['port'], 
        #                                             self.jsonConfigurationPlugin['baud_rate'], 
        #                                             self.jsonConfigurationPlugin['byte_size'],
        #                                             self.jsonConfigurationPlugin['parity'],
        #                                         self.jsonConfigurationPlugin['stop_bits']
        #                                         )
        # else:
        self.windows_serial_port_manager = WindowsAsyncSerialManager(self.jsonConfigurationPlugin['port'])       
        
        if (Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX):
            result_connect = self.linux_serial_port_manager.connect()
            self.linux_serial_port_manager.start_communication()
        else:
            result_connect = self.windows_serial_port_manager.open_port()
            
        if result_connect:
            # If connected, send the data
            json_data = job["printData"]

            # is_valid, result = Utilities.validate_json(json_data)
            # if is_valid:
            #     print("Valid JSON")
            # else:
            #     status_result = "400"
            #     self.logger.info(f"Processing {self.plugin_name} invalid JSON {result}")
            #     return status_result

            try:
                zpl_content = self.json_to_zpl(json_data)
                
            except ValueError as e:
                status_result = "400"
                self.logger.info(f"Processing {self.plugin_name} error converting JSON to ZPL JSON {e}")
                return status_result

            try:
                result_send_data = ""
                
                if (Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX):
                    result_send_data = self.linux_serial_port_manager.send_data(zpl_content.encode())
                else:
                    # result_send_data = self.windows_serial_port_manager.send_data(zpl_content.encode())
                        # Start listening for incoming data (asynchronously)
                    listen_task = asyncio.create_task(self.windows_serial_port_manager.start_listening(self.handle_received_data))

                    self._running = True
                    
                    while self._running:
                        # Send some data asynchronously
                        self.windows_serial_port_manager.send_data("Hello from asyncio!")
                        
                        if (self._running == False):
                            break
                        
                        time.sleep(0.1)
                        
                
                status_result = "200" if result_send_data else "400"
            except Exception as e:
                self.logger.info(f"Error processing {self.plugin_name} in ZPL JSON {e}")
                status_result = "400"
            finally:
                if (Utilities.getOperatingSystemType() == OPERATING_SYSTEM_TYPE.LINUX):
                    self.linux_serial_port_manager.stop_communication()
                    self.linux_serial_port_manager.disconnect()
                else:
                    self.windows_serial_port_manager.close_port()
        else:
            status_result = "400"

        self.linux_serial_port_manager = None
        self.windows_serial_port_manager = None
            
        self.logger.info(f"Processing {self.plugin_name} result {status_result}")
        return status_result

    def json_to_zpl(self, json_data):
        """
        Convert the json to zpl commands

        Args:
            data (str): json dictionary

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: ZPL string
        """
        zpl = "^XA\n"

        # iterate throw json
        
        for data in json_data:
        
            # Basic validation
            if not isinstance(data, dict):
                raise ValueError("Invalid JSON: expected a dictionary.")

            # Text
            if 'text' in data:
                text = data['text']
                x = data.get('x', 50)
                y = data.get('y', 50)
                font_size = data.get('font_size', 50)
                orientation = data.get('orientation', 'N')  # N: normal, R: rotacionado 90, I: invertido 180, B: rotacionado 270
                
                if orientation not in ['N', 'R', 'I', 'B']:
                    raise ValueError(f"Invalid text orientation: {orientation}")
                
                zpl += f"^FO{x},{y}\n^A0{orientation},{font_size},{font_size}\n^FD{text}^FS\n"

            # Barcode
            if 'barcode' in data:
                barcode = data['barcode']
                x = data.get('barcode_x', 50)
                y = data.get('barcode_y', 150)
                barcode_type = data.get('barcode_type', 'Code128')
                height = data.get('barcode_height', 100)
                if barcode_type == 'Code128':
                    zpl += f"^FO{x},{y}\n^B3N,N,{height},Y,N\n^FD{barcode}^FS\n"
                elif barcode_type == 'QR':
                    zpl += f"^FO{x},{y}\n^BQN,2,10\n^FDLA,{barcode}^FS\n"
                elif barcode_type == 'Code39':
                    zpl += f"^FO{x},{y}\n^B3N,N,{height},Y,N\n^FD{barcode}^FS\n"
                else:
                    raise ValueError(f"Unsupported barcode type: {barcode_type}")

            # Image
            if 'image' in data:
                image_base64 = data['image']
                x = data.get('image_x', 50)
                y = data.get('image_y', 300)
                try:
                    image_data = base64.b64decode(image_base64)
                    image_hex = binascii.hexlify(image_data).decode('utf-8').upper()
                    bytes_per_row = len(image_data) // len(data.get('image_height', [1]))
                    zpl += f"^FO{x},{y}\n^GFA,{len(image_hex)},{len(image_hex)},{bytes_per_row},{image_hex}^FS\n"
                except binascii.Error as e:
                    raise ValueError(f"Error decoding the image: {e}")
        
            zpl += "^XZ"
        
        return zpl

    async def handle_received_data(self, data):
        """Callback function to handle received data."""
        print(f"Received data: {data}")
        time.sleep(4)
        self._running = False
        
# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, LabelPlugin())