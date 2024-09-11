# controller/plugins/label_plugin.py
import base64
import binascii
import json
import os
from controller.plugin_base import PluginBase

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class LabelPlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Label plugin class by calling the base class initializer.
        """
        super().__init__(os.path.join(os.path.dirname(__file__)))

    def process(self, job):
        """
        Process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"Processing {self.plugin_name} Job {job['jobId']}")

        # initialize ok
        status_result = "200"
        
        # Connect to serial port
        result_connect = self.serial_port_manager.connect()

        if result_connect:
            # If connected, send the data
            json_data = job["printData"]

            try:
                data = json.loads(json_data)
            except json.JSONDecodeError as e:
                status_result = "400"
                self.logger.info(f"Processing {self.plugin_name} invalid JSON {e}")
                return status_result

            try:
                # Exemple
                # json_data = '''
                # {
                # "text": "Hello, World!",
                # "x": 100,
                # "y": 150,
                # "font_size": 40,
                # "orientation": "R",
                # "barcode": "1234567890",
                # "barcode_type": "QR",
                # "barcode_x": 200,
                # "barcode_y": 300
                # }
                # '''
                zpl_content = self.json_to_zpl(data)
            except ValueError as e:
                status_result = "400"
                self.logger.info(f"Processing {self.plugin_name} error converting JSON to ZPL JSON {e}")
                return status_result

            try:
                self.serial_port_manager.start_communication()

                result_send_data = self.serial_port_manager.send_data(zpl_content.encode())

                status_result = "200" if result_send_data else "400"
            except:
                status_result = "400"
            finally:
                self.serial_port_manager.stop_communication()
                self.serial_port_manager.disconnect()
        else:
            status_result = "400"

        self.logger.info(f"Processing {self.plugin_name} result {status_result}")
        return status_result

    def json_to_zpl(self, data):
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

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, LabelPlugin())