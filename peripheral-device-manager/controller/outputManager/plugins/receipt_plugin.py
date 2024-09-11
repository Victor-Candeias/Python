# controller/plugins/receipt_plugin.py
import json
import os
from tkinter import Image
from controller.plugin_base import PluginBase

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class ReceiptPlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Receipt plugin class by calling the base class initializer.
        """
        super().__init__(os.path.join(os.path.dirname(__file__)))
        
    def process(self, job):
        """
        Process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"Processing {self.plugin_name} Job {job['job_id']}")

        # initialize ok
        status_result = "200"
        
        # Connect to serial port
        result_connect = self.serial_port_manager.connect()

        if result_connect:
            self.serial_port_manager.start_communication()

            try:
                # Exemple
                # json_input = '''
                #     {
                #         "items": [
                #             {"type": "text", "text": "Olá, Mundo!", "x": 0, "y": 0, "font_size": "large"},
                #             {"type": "barcode", "data": "1234567890", "x": 0, "y": 30},
                #             {"type": "qrcode", "data": "https://example.com", "x": 0, "y": 100},
                #             {"type": "image", "path": "image.png", "x": 0, "y": 200}
                #         ]
                #     }
                # '''
                self.initialize_printer()
                
                # If connected, send the data
                self.process_json(job["printData"])
            except:
                status_result =  "400"
            finally:
                self.serial_port_manager.stop_communication()
                self.serial_port_manager.disconnect()
        else:
            # Connection failed
            status_result = "400"

        self.logger.info(f"Processing {self.plugin_name} result {status_result}")
        return status_result

    def process_json(self, json_data):
        """
        Processes JSON and prints as specified
        """
        data = json.loads(json_data)

        for item in data['items']:
            if item['type'] == 'text':
                self.print_text(item['text'], item['x'], item['y'], item['font_size'])
            elif item['type'] == 'barcode':
                self.print_barcode(item['data'], item['x'], item['y'], item.get('width', 2), item.get('height', 162))
            elif item['type'] == 'qrcode':
                self.print_qrcode(item['data'], item['x'], item['y'], item.get('size', 3))
            elif item['type'] == 'image':
                self.print_image(item['path'], item['x'], item['y'])
            else:
                print(f"Unknown item type: {item['type']}")

    def send_command(self, command):
        """
        Sends an ESC/POS command to the printer
        """
        self.serial_port_manager.send_data(command)
        
    def initialize_printer(self):
        """
        Initialize the printer
        """
        self.send_command(b'\x1B\x40')  # ESC @

    def print_image(self, image_path, x, y):
        """
        Prints an image at the specified position
        """
        img = Image.open(image_path)
        img = img.convert('1')  # Converts to black and white
        img = img.resize((img.width // 8, img.height))
        width, height = img.size
        pixels = img.tobytes()
        self.send_command(b'\x1B\x40')  # ESC @
        # Sends the image (command details may vary depending on the printer model)
        self.send_command(b'\x1D\x76\x30\x00' + width.to_bytes(2, 'little') + height.to_bytes(2, 'little') + pixels)

    def print_qrcode(self, data, x, y, size=3):
        """
        Prints a QR Code at the specified position
        """
        self.send_command(b'\x1B\x40')  # ESC @
        self.send_command(b'\x1D\x28\x6B\x03\x00\x31\x43' + size.to_bytes(1, 'little'))  # QR Code Size
        self.send_command(b'\x1D\x28\x6B\x03\x00\x31\x45\x00')  # Error correction level
        self.send_command(b'\x1D\x28\x6B' + (len(data) + 3).to_bytes(1, 'little') + b'\x31\x50\x30' + data.encode())  # QR Code Data
        self.send_command(b'\x1D\x28\x6B\x03\x00\x31\x51\x30')  # Print the QR Code

    def print_barcode(self, data, x, y, width=2, height=162):
        """
        Prints a barcode at the specified position
        """
        self.send_command(b'\x1B\x40')  # ESC @
        self.send_command(b'\x1D\x6B\x02')  # Barcode
        self.send_command(width.to_bytes(1, 'little'))  # Width
        self.send_command(height.to_bytes(1, 'little'))  # Height
        self.send_command(data.encode() + b'\n')

    def print_text(self, text, x, y, font_size):
        """
        Prints text at specified position with font size
        """
        # Depending on your printer model, you may need to adjust these commands
        self.send_command(b'\x1B\x40')  # ESC @ (Initialize the printer)
        # Adjust the position (e.g. setting the cursor to x and y, if supported)
        self.send_command(b'\x1B\x24' + x.to_bytes(2, 'little') + y.to_bytes(2, 'little'))
        # Adjust font size (this command may vary between models)
        if font_size == 'small':
            self.send_command(b'\x1D\x21\x00')  # Small font
        elif font_size == 'large':
            self.send_command(b'\x1D\x21\x11')  # Large font
        self.send_command(text.encode() + b'\n')

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, ReceiptPlugin())
