import logging
from pymongo import MongoClient

class MongoDBHandler(logging.Handler):
    def __init__(self, db_uri, db_name, collection_name):
        logging.Handler.__init__(self)
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def emit(self, record):
        log_entry = self.format(record)
        self.collection.insert_one({"log": log_entry})

    def close(self):
        self.client.close()
        logging.Handler.close(self)

# Example usage
if __name__ == "__main__":
    # MongoDB connection details
    db_uri = "mongodb://localhost:27017/"
    db_name = "logging_db"
    collection_name = "logs"

    # Create a logger
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)

    # Create and configure MongoDBHandler
    mongo_handler = MongoDBHandler(db_uri, db_name, collection_name)
    mongo_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Add the MongoDB handler to the logger
    logger.addHandler(mongo_handler)

    # Log some messages
    logger.info("This is an info message.")
    logger.error("This is an error message.")
