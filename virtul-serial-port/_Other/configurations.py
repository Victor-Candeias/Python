from pymongo import MongoClient

# MongoDB connection details
db_uri = "mongodb://localhost:27017/"
db_name = "serial_port_db"
collection_name = "virtual_ports"

# Connect to MongoDB
client = MongoClient(db_uri)
db = client[db_name]
collection = db[collection_name]

# Example configuration document
virtual_port_config = {
    "port_name": "COM3",
    "real_port": "COM1",
    "baud_rate": 9600,
    "data_bits": 8,
    "parity": "N",
    "stop_bits": 1,
    "flow_control": "None",
    "enabled": True
}

# Insert a new virtual port configuration
def insert_config(config):
    collection.insert_one(config)
    print("Configuration inserted.")

# Retrieve a virtual port configuration by port name
def get_config(port_name):
    config = collection.find_one({"port_name": port_name})
    if config:
        print("Configuration found:", config)
    else:
        print("No configuration found.")

# Update a virtual port configuration
def update_config(port_name, update_fields):
    result = collection.update_one({"port_name": port_name}, {"$set": update_fields})
    if result.matched_count > 0:
        print("Configuration updated.")
    else:
        print("No configuration found to update.")

# Delete a virtual port configuration
def delete_config(port_name):
    result = collection.delete_one({"port_name": port_name})
    if result.deleted_count > 0:
        print("Configuration deleted.")
    else:
        print("No configuration found to delete.")

# Example usage
if __name__ == "__main__":
    # Insert a new configuration
    insert_config(virtual_port_config)

    # Retrieve a configuration
    get_config("COM3")

    # Update the configuration
    update_fields = {"baud_rate": 115200}
    update_config("COM3", update_fields)

    # Delete the configuration
    delete_config("COM3")
