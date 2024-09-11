
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from config import Config

def setup_logging(logToConsole: bool = False):
    """
    Setup the log config
    """
    
    # set the log directory
    log_directory = Config._instance.LOG_FILES_DIRECTORY
        
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # define the log file name with the current date
    log_filename = datetime.now().strftime("%Y-%m-%d.log")
    log_filepath = os.path.join(log_directory, log_filename)
    
    # add log file handler
    handlers_list = [TimedRotatingFileHandler(log_filepath, when="midnight", interval=1, backupCount=7)]
    
    if (logToConsole):
        # also log to console
        handlers_list.append(logging.StreamHandler())
        
    # set up the root logger
    logging.basicConfig(
    level=logging.INFO,  # set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=handlers_list
    )