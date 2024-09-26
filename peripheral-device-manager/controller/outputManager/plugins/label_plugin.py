# controller/plugins/label_plugin.py
import asyncio
import base64
import binascii
import json
import logging
import os
import time
from controller.plugin_base import PluginBase
from controller.utilities import Utilities, OPERATING_SYSTEM_TYPE

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class LabelPlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Label plugin class by calling the base class initializer.
        """
        self.logger = logging.getLogger(__name__)
        
        pluginDir = os.path.join(os.path.dirname(__file__), f"{self.__class__.plugin_name}.json")
        
        self.logger.info(f"{PluginBase.plugin_name};__init__();pluginDir={pluginDir}")
        
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
        self._running = False
    
    def process(self, job):
        """
        Process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"{PluginBase.plugin_name}.py;process();job={job}")

        # initialize ok
        status_result = "200"
            
        # If connected, send the data
        json_data = job["printData"]

        self.logger.info(f"{PluginBase.plugin_name}.py;process();json_data={json_data}")
        
        try:
            zpl_content = self.json_to_zpl(json_data)
            
            # Open the serial port with retries
            if self.serial_manager != None:    
                # start running
                self._running = True
                
                # Start listening for data and provide a callback function
                self.serial_manager.start_listening(self.data_callback)

                # Send data via serial port
                self.serial_manager.send_data(zpl_content)

                # Pause for a few seconds to allow data to be received
                        # O programa ficará em execução até que o callback detecte o evento de parada
                while self._running:
                    time.sleep(1)

                # Stop listening and close the port
                self.serial_manager.stop_listening()
                self.serial_manager.close_port()
            
        except ValueError as e:
            status_result = "400"
            self.logger.info(f"Processing {self.plugin_name} error converting JSON to ZPL JSON {e}")
            
            return json.dumps({"status": status_result, "error": e})
 
        return json.dumps({"status": status_result, "job": job, "job_result": self.result_data_read})

    def data_callback(self, data):
        # save result data
        self.result_data_read = data
        print(f"Data received from callback: {self.result_data_read}")
        self._running = False
        
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
        
# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, LabelPlugin())