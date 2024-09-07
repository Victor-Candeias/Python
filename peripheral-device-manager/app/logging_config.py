
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logging():
    """
    setup_logging _summary_
    """
    log_directory = r"C:\\logfiles\\DeviceManager"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # Define the log file name with the current date
    log_filename = datetime.now().strftime("%Y-%m-%d.log")
    log_filepath = os.path.join(log_directory, log_filename)
    
    # Set up the root logger
    logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        TimedRotatingFileHandler(log_filepath, when="midnight", interval=1, backupCount=7),
        logging.StreamHandler()  # Also log to console
        ]
    )