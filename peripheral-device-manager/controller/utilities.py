import importlib
import json
import os
from controller.plugin_registry import PluginRegistry
import messages
from enum import Enum

# operating system enum
class OPERATING_SYSTEM_TYPE(Enum):
    WINDOWS = 1
    LINUX = 2
    
class Utilities:
    @staticmethod
    def registerPlugins(plugins_dir, logger, inputType):
        """
        Automatically discover and register all output plugins in the plugins directory.

        Args:
            plugins_dir (str): Location of the plugins
            logger (class): Instance of the log
            inputType (str): Type of plugin to be resisted

        Returns:
            list: return the list of founded plugins
        """
        localPlugin = {}

        for filename in os.listdir(plugins_dir):
            if filename.endswith('.py') and filename not in ('plugin_base.py', '__init__.py'):
                module_name = f"controller.{inputType}.plugins.{filename[:-3]}"
                
                logger.info(f"_register_all_plugins();module_name {module_name}")
                
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    
                    # Import PluginBase here to avoid circular import at the top
                    from controller.plugin_base import PluginBase
                    
                    if isinstance(attr, type) and issubclass(attr, PluginBase) and attr is not PluginBase:
                        plugin_instance = attr()
                        plugin_type = plugin_instance.get_type()
                        localPlugin[plugin_type] = plugin_instance
                        
                        logger.info(f"Registered plugin: {plugin_type}")
                        
                        PluginRegistry.register_plugin(plugin_type, plugin_instance)

        return localPlugin
    
    @staticmethod
    def sendDataToClients(hostUrl, sessionId, inputType, message):
        # Send data to WebSocket
        from controller.websocket_manager.websocket_client import WebSocketClient
        
        # Create a WebSocketClient instance
        client = WebSocketClient(hostUrl)  # Replace with your server URL request.host_url
        
        filters=[sessionId, inputType]
        
        # Connect to the server with session ID and filters
        client.connect(filters=filters)
        
        # client.send_message(message)
        client.send_message_to_rooms(filters, message)
        
        # Keep the client running to listen for events
        client.keep_running(waitTimeToExit=2)
        
        client.disconnect()
        
    @staticmethod
    def getOperatingSystemType():
        import os

        if os.name == 'nt':
            return OPERATING_SYSTEM_TYPE.WINDOWS
        else:
            return OPERATING_SYSTEM_TYPE.LINUX
        
    @staticmethod
    def validate_json(json_string):
        try:
            json_object = json.loads(json_string)
            return True, json_object  # JSON is valid
        except json.JSONDecodeError as e:
            return False, str(e)  # JSON is invalid, return the error message