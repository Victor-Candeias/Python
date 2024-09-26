# server/controllers/device_manager.py
from flask import json



class DeviceManager:
    def __init__(self) -> None:
        # load all plugin config
        from controllers import ConfigurationManager
        
        config = ConfigurationManager()
        
        self.pluginConfig = config.list_devices()
        
        print()