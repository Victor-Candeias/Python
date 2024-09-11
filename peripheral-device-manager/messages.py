# messages.py

import os
import json

class Messages:
    # instance of the singleton
    _instance = None

    # --------------------------------------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        # create the singleton
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
       
    # --------------------------------------------------------------------------------------------------
    def __init__(self):
        # get the current file directory
        self.directory = os.path.join(os.path.dirname(__file__))
        
        # get the current config file
        self.file_name = os.path.splitext(os.path.basename(__file__))[0] + ".json"
        
        # full path of the config file
        self.full_name = os.path.join(self.directory, self.file_name)
        
        if os.path.exists(self.full_name):
            with open(self.full_name, 'r') as file:
                data = json.load(file)
                
                # get the json dic keys
                config_keys = data.keys()
                
                # open file a create all properties from keys
                for k in config_keys:
                    setattr(self, k, data.get(k))

# initialize the singleton
messages = Messages()
