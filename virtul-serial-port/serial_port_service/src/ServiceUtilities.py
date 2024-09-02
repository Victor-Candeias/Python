import datetime
import os
import logging
import json
from pathlib import Path

# Example usage:
# ServiceUtilities.setup_logging()
# config = ServiceUtilities.load_config()
LOG_FILE_DIRECTORY = "C:\logfiles\serialportservice"
BASE_FILE_NAME = 'SerialPortService'

class ServiceUtilities:
    @staticmethod
    def get_file_name():
        """Set up logging configuration."""
        # check if dir exists
        ServiceUtilities.ensure_directory_exists(LOG_FILE_DIRECTORY)
        
        current_date = datetime.datetime.now().strftime("%y%m%d")
        log_filename = f"{current_date}_{BASE_FILE_NAME}.log"

        return "{}{}{}".format(LOG_FILE_DIRECTORY, "\\", log_filename)

    @staticmethod
    def write_log_info(message):
        """Write log info."""
        fileName = ServiceUtilities.get_file_name()
        
        with open(fileName, 'a+') as f:
            f.write("Info;" + message + "\n")
 
    @staticmethod
    def write_log_error(message):
        """Write log error."""
        with open(ServiceUtilities.get_file_name(), 'a+') as f:
            f.write("Error;" + message + "\n")
               
    @staticmethod
    def load_config():
        """Load configuration from a JSON file."""
        config_path = os.path.join(os.path.dirname(__file__), 'config\config.json')
        with open(config_path, 'r') as config_file:
            logging.info(f"Loading configuration from {config_path}.")
            return json.load(config_file)

    @staticmethod
    def ensure_directory_exists(directory_path):
        """Check if a directory exists, and create it if it does not."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

