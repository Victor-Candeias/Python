# controller/plugins/label_plugin.py
from controller.plugin_base import PluginBase
# Register the plugin
import logging

class BarcodePlugin(PluginBase):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"BarcodePlugin();")

    def process(self, job):
        print(f"Processing Barcode Job {job['job_id']} on Barcode Reader...")
        result = {"status": "200"}
        return result
    
    def get_type(self):
        return "barcode"
    
    def is_synchronous(self):
        return True

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin("label", BarcodePlugin())

