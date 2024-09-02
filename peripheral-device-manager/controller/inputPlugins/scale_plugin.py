# controller/plugins/label_plugin.py
from controller.plugin_base import PluginBase
# Register the plugin
import logging

class ScalePlugin(PluginBase):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"ScalePlugin();")

    def process(self, job):
        print(f"Processing Scale Job {job['job_id']} on Scale Reader...")
        result = {"status": "200"}
        return result
    
    def get_type(self):
        return "scale"
    
    def is_synchronous(self):
        return True

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin("label", ScalePlugin())

