# controller/plugin_base.py
import logging
import json
import os
import threading
from messages import Messages

class PluginBase:
    # Class-level variable to hold the plugin name
    plugin_name = ""

    def __init__(self, pluginDirectory=None):
        """
        Initialize the base class, set up logging, and load the configuration.

        Args:
            directory (str): Plugin directory
        """
        self.logger = logging.getLogger(__name__)
        self.jsonConfigurationPlugin = ''
        
        # Serial port manager will be set by the derived class
        self._running = False
        
        if (pluginDirectory!=None):
            # load configuration
            self._load_configuration(pluginDirectory)
            
            if (self.jsonConfigurationPlugin != '' and self.jsonConfigurationPlugin['autoStart'] == "true"):
                try:
                    self.start()
                except ValueError as e:
                    # log
                    
                    self.stop()
    
    # ----------------------------------------------------------------------------------------
    def _load_configuration(self, jasonConfigFile):
        """
        Load the plugin configuration from a JSON file.
        """
        if os.path.exists(jasonConfigFile):
            with open(jasonConfigFile, 'r') as file:
                self.jsonConfigurationPlugin = json.load(file)
                self.logger.info(f"plugin_base.py;load_configuration();jsonConfigurationPlugin={self.jsonConfigurationPlugin}")
        else:
            self.logger.error("plugin_base.py;load_configuration();Plugin {PluginBase.plugin_name} config not found! ()")

    # ----------------------------------------------------------------------------------------
    def start(self):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError(Messages.NOT_IMPLEMENTED)
        # self._running = True
        # self._thread = threading.Thread(target=self.read_from_serial)
        # self._thread.start()
        
        # self.logger.info("plugin_base.py;start();Start thread={PluginBase.plugin_name}.")
    
    # ----------------------------------------------------------------------------------------   
    def stop(self):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError(Messages.NOT_IMPLEMENTED)
        # self._running = False
        # if self._thread.is_alive():
        #     self._thread.join()
        
        # se#lf.logger.info("plugin_base.py;stop();Stop thread={PluginBase.plugin_name}.")
        
    # def read_from_serial(self):
    #     """
    #     Abstract method to be implemented by derived classes.
    #     """
    #     raise NotImplementedError(Messages.NOT_IMPLEMENTED)
    
    # ----------------------------------------------------------------------------------------    
    def process(self, job = None):
        """
        Abstract method to be implemented by derived classes.
        """
        raise NotImplementedError(Messages.NOT_IMPLEMENTED)
    
    # ----------------------------------------------------------------------------------------    
    def get_type(self):
        """
        Return the plugin name.
        """
        return self.__class__.plugin_name
