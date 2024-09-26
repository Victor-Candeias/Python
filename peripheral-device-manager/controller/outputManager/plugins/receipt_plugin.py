# controller/plugins/receipt_plugin.py
import json
import logging
import os
import time
from tkinter import Image
from controller.plugin_base import PluginBase
from controller.utilities import Utilities, OPERATING_SYSTEM_TYPE

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class ReceiptPlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Receipt plugin class by calling the base class initializer.
        """
        self.logger = logging.getLogger(__name__)
        
        pluginDir = os.path.join(os.path.dirname(__file__), f"{self.__class__.plugin_name}.json")
        
        self.logger.info(f"{PluginBase.plugin_name};__init__();pluginDir={pluginDir}")
        
        self.finish_send_data = False
        
        self.result_data_read = ""
        
        super().__init__(pluginDir)

    def start(self):
        """
        _summary_
        """
        from controller.serialPortManager.serial_port_manager import SerialManager

        # get serial port config
        serialPortConfig = self.jsonConfigurationPlugin["serialPortConfig"]
        
        # Create SerialManager instance for COM9 port
        self.serial_manager = SerialManager(serialPortConfig["port"])
         
                                            # serialPortConfig["baud_rate"],
                                            # serialPortConfig["byte_size"], 
                                            # serialPortConfig["parity"],
                                            # serialPortConfig["stop_bits"])

        # Open the serial port with retries
        if not self.serial_manager.open_port(): 
            # error 
            raise Exception(f"Error starting Serial port on {serialPortConfig["port"]}")

    def stop(self):
        # self._running = False
        self.finish_send_data = False
        
    def process(self, job):
        """
        Process the given job and handle the serial connection and data transmission.
        """
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
        self.logger.info(f"{PluginBase.plugin_name};process();job={job}")

        # initialize ok
        json_data_result = ""
            
        # If connected, send the data
        json_data = job["printData"]

        self.logger.info(f"{PluginBase.plugin_name}.py;process();json_data={json_data}")
        
        try:
            # Open the serial port with retries
            if self.serial_manager != None:    
                # start running
                # self._running = True
                
                # Start listening for data and provide a callback function
                self.serial_manager.start_listening(self.data_callback)

                self.initialize_printer()
                
                json_data_result = self.process_json(json_data)
                
                # finish send data
                self.finish_send_data = True
            
                # Pause for a few seconds to allow data to be received
                while not self.finish_send_data:
                    time.sleep(1)
            
                json_data_result = json.dumps({"status": status_result, "job": job, "job_result": self.result_data_read})
                
        except ValueError as e:
            status_result = "400"
            self.logger.info(f"Processing {self.plugin_name} error converting JSON to ZPL JSON {e}")
            
            json_data_result = json.dumps({"status": status_result, "error": e})
 
        # Stop listening and close the port
        self.serial_manager.stop_listening()
        self.serial_manager.close_port()
                
        return json_data_result

    def data_callback(self, data):
        # save result data
        self.result_data_read = self.result_data_read + "\n" + data
        print(f"Data received from callback: {self.result_data_read}")
        # self._running = False

    def process_json(self, json_data):
        """
        Processes JSON and prints as specified
        """
        self.logger.info(f"{PluginBase.plugin_name};process_json();json_data={json_data}")
        
        # data = json.loads(json_data)

        for item in json_data: #['items']:
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
        # Send data via serial port
        self.serial_manager.send_data(command.decode())
        
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
