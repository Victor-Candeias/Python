# server/controllers/mongodb_handler.py
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBHandler:
    def __init__(self, db_name: str, collection_name: str, uri: str = "mongodb://localhost:27017/"):
        # Initialize MongoDB connection
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_item(self, item: dict) -> str:
        """Insert a new item into the collection."""
        result = self.collection.insert_one(item)
        return str(result.inserted_id)

    def get_item(self, item_id: str) -> dict:
        """Retrieve an item by its ID."""
        return self.collection.find_one({"_id": ObjectId(item_id)})

    def update_item(self, item_id: str, update_fields: dict) -> dict:
        """Update an item in the collection."""
        result = self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_fields}
        )
        if result.modified_count > 0:
            return self.get_item(item_id)
        return None

    def delete_item(self, item_id: str) -> bool:
        """Delete an item by its ID."""
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def list_items(self) -> list:
        """List all items in the collection."""
        return list(self.collection.find())

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()