# controller/plugin_base.py
import logging
import json
import os
# from controller.serialPortManager.windows_serial_port_manager import WindowsAsyncSerialManager
# from controller.serialPortManager.linux_serial_connection_manager import LinuxSerialPortManager
from messages import Messages

class PluginBase:
    # Class-level variable to hold the plugin name
    plugin_name = ""

    def __init__(self, directory=None):
        """
        Initialize the base class, set up logging, and load the configuration.

        Args:
            directory (str): Plugin directory
        """
        self.logger = logging.getLogger(self.__class__.plugin_name)
        self.jsonConfigurationPlugin = ''
        self.messages = Messages
        
        if (directory != None):
            # Path of the config file based on the plugin name
            self.configFilePath = os.path.join(directory, f"{self.__class__.plugin_name}.json")

            # Serial port manager will be set by the derived class
            self.linux_serial_port_manager = None
            self.windows_serial_port_manager = None
            self._running = False
        
            # Load configuration
            self.load_configuration()

    def load_configuration(self):
        """
        Load the plugin configuration from a JSON file.
        """
        if os.path.exists(self.configFilePath):
            with open(self.configFilePath, 'r') as file:
                self.jsonConfigurationPlugin = json.load(file)
                self.logger.info(f"Loaded configuration: {self.jsonConfigurationPlugin}")
        else:
            self.logger.error("Plugin config not found! ()" + self.configFilePath + ")")
    
    def process(self, job = None):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError(self.messages.NOT_IMPLEMENTED)

    def start(self):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError(self.messages.NOT_IMPLEMENTED)

    def stop(self):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError(self.messages.NOT_IMPLEMENTED)
          
    def get_type(self):
        """
        Return the plugin name.
        """
        return self.__class__.plugin_name
