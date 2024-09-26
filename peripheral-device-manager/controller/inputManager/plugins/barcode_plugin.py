# controller/plugins/barcode_plugin.py
import json
import logging
import os
import threading
import time
from controller.plugin_base import PluginBase
from config import Config
from messages import Messages
from controller.utilities import Utilities, OPERATING_SYSTEM_TYPE

# set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class BarcodePlugin(PluginBase):
    def __init__(self):
        """
        initialize the Barcode plugin class by calling the base class initializer.
        """
        self.logger = logging.getLogger(__name__)
        
        pluginDir = os.path.join(os.path.dirname(__file__), f"{self.__class__.plugin_name}.json")
        
        self.logger.info(f"{PluginBase.plugin_name};__init__();pluginDir={pluginDir}")
        
        super().__init__(pluginDir)
        
    def read_from_serial(self):
        """
        process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"{PluginBase.plugin_name}.py;read_from_serial();plugin_name={self.plugin_name}")
        
        status_result = "200"

        # simulate data
        data = {"status": status_result, "Message": "This is a message from plugin {PluginBase.plugin_name}"}
        
        try:
            # call websocket
            from controller.utilities import Utilities
        
            resultStatus = Messages._instance.STATUS_RESULT_OK
        
            try:
                serverUrl = Config._instance.PROTOCOL + Config._instance.HOST + ":" + Config._instance.PORT
                
                Utilities.sendDataToClients(serverUrl, sessionId=None, inputType=PluginBase.plugin_name, message=data)
            except:
                resultStatus = Messages._instance.STATUS_RESULT_ERROR

            # return result
            return json.dumps({'status': 'success', 'message': 'Input data sent to WebSocket clients'}), resultStatus
        
        except ValueError as e:
            self.logger.error(f"{PluginBase.plugin_name}.py;read_from_serial()=error={e}")
            return None

# register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, BarcodePlugin())
