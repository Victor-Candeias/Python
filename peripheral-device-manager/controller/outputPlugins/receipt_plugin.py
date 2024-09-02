# controller/plugins/receipt_plugin.py
import logging
from controller.plugin_base import PluginBase

class ReceiptPlugin(PluginBase):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"LabelPlugin();")
        
    def process(self, job):
        print(f"Processing Receipt Job {job['job_id']} on Receipt Printer...")
        result = {"status": "200"}
        return result #f"Receipt Job {job['job_id']} processed successfully"
    
    def get_type(self):
        return "receipt"
    
    def is_synchronous(self):
        return True

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin("receipt", ReceiptPlugin())
