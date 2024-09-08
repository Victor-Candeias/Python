# controller/plugin_base.py
import logging
import json
import os

from controller.serialPortManager.serial_connection_manager import SerialConnectionManager

class PluginBase:
    # Class-level variable to hold the plugin name
    plugin_name = ""

    def __init__(self, directory):
        """
        Initialize the base class, set up logging, and load the configuration.
        """
        self.logger = logging.getLogger(self.__class__.plugin_name)

        # Path of the config file based on the plugin name
        self.configFilePath = os.path.join(directory, f"{self.__class__.plugin_name}.json")

        # Serial port manager will be set by the derived class
        self.serial_port_manager = None

        self._running = False
        
        # Load configuration
        self.load_configuration()

    def load_configuration(self):
        """
        Load the plugin configuration from a JSON file.
        """
        if os.path.exists(self.configFilePath):
            with open(self.configFilePath, 'r') as file:
                data = json.load(file)
                self.logger.info(f"Loaded configuration: {data}")

                # Initialize the serial port manager
                self.serial_port_manager = SerialConnectionManager(
                    data['port'], 
                    data['baud_rate'], 
                    data['byte_size'],
                    data['parity'],
                    data['stop_bits']
                )
        else:
            self.logger.error(f"Configuration file not found: {self.configFilePath}")
    
    def process(self, job = None):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError("Derived classes must implement this method")

    def start(self):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError("Derived classes must implement this method")

    def stop(self):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError("Derived classes must implement this method")
          
    def get_type(self):
        """
        Return the plugin name.
        """
        return self.__class__.plugin_name
