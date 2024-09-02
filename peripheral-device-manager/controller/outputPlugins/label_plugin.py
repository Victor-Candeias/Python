# controller/plugins/label_plugin.py
from controller.plugin_base import PluginBase
# Register the plugin
import logging

class LabelPlugin(PluginBase):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"LabelPlugin();")

    def process(self, job):
        print(f"Processing Label Job {job['job_id']} on Label Printer...")
        result = {"status": "200"}
        return result #f"Label Job {job['job_id']} processed successfully"
    
    def get_type(self):
        return "label"
    
    def is_synchronous(self):
        return True

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin("label", LabelPlugin())

