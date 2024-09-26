# server/controllers/configuration_manager.py
from bson import ObjectId
from flask import json, jsonify
from controllers.mongodb_handler import MongoDBHandler

class ConfigurationManager:
    def __init__(self) -> None:
        self.mongodb = MongoDBHandler(db_name="peripheral_device_manager", collection_name="device_manager")

    def create_device(self, device_data: dict) -> str:
        device = self.mongodb.add_item(device_data)
        if device:
            return str(device)
        raise Exception("Error saving Device configuration!")        

    def get_device(self, device_id: str) -> str:
        device = self.mongodb.get_item(device_id)
        if device:
            device['_id'] = str(device['_id'])
            return str(device)
        raise Exception("Device configuration not found!")

    def delete_device(self, device_id: str) -> bool:
        return self.mongodb.delete_item(device_id)

    def list_devices(self) -> list:
        # Convert data
        converted_data = self.convert_objectid_to_string(self.mongodb.list_items())

        # Convert to JSON
        json_data = json.dumps(converted_data)
        json_data = json.loads(json_data)
    
        return json_data #self.mongodb.list_items()
    
    def convert_objectid_to_string(self, data):
        for item in data:
            if '_id' in item and isinstance(item['_id'], ObjectId):
                item['_id'] = str(item['_id'])  # Convert ObjectId to string
        return data