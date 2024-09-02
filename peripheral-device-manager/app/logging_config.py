# Purpose of app/logging_config.py
# Centralized Logging Configuration:

# This file provides a centralized place to configure how logging should work across the application. This includes setting log levels, formatting log messages, and determining where logs should be output (e.g., to a file, console, or external logging service).
# Custom Logging Setup:

# You can customize logging behavior depending on the environment (e.g., different logging settings for development, testing, and production). This might involve different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) or different log outputs.
# Log File Management:

# You can configure logging to write to a specific file or set up log rotation to prevent log files from growing indefinitely.

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logging():
    # Create a logs directory if it doesn't exist
    log_directory = r"C:\logfiles\DeviceManager"
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
        TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7),
        logging.StreamHandler()  # Also log to console
        ]
    )
    
    # logging.basicConfig(
    #     level=logging.INFO, # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    #     filename=log_filepath,
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    # )
