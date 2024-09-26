from controllers.mongodb_handler import MongoDBHandler

class ConfigurationManager:
    def __init__(self) -> None:
        # mongoDb
        self.mongodb = MongoDBHandler(db_name="peripheral_device_manager", collection_name="device_manager")
