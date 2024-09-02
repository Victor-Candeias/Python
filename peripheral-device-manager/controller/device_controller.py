# controller/device_controller.py

import logging
import uuid

logger = logging.getLogger(__name__)

# Simulate a list of devices
devices = ["Printer A", "Printer B", "Scale A", "Barcode Reader A"]
# Simulate event channels
event_channels = {}

# Get all devices
def list_all_devices():
    logger.info("Listing all devices")
    return devices
 #
def create_input_job(data):
    input_job_id = str(uuid.uuid4())
    # Simulate processing the input job (e.g., sending data to a scale or barcode reader)
    logger.info(f"Created input job: {input_job_id} with data: {data}")
    return input_job_id
