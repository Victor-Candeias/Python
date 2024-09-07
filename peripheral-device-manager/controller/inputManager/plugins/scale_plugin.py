# controller/plugins/scale_plugin.py
import os
from controller.plugin_base import PluginBase

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class ScalePlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Scale plugin class by calling the base class initializer.
        """
        super().__init__(os.path.join(os.path.dirname(__file__)))
        
    def process(self):
        """
        Process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"Processing {self.plugin_name} Job {job['job_id']}")

        # Connect to serial port
        result_connect = self.serial_port_manager.connect()
        status_result = "200"

        if result_connect:
            # If connected, send the data
            result_send_data = self.serial_port_manager.send_data(job["printData"])
            if not result_send_data:
                status_result = "404"
        else:
            # Connection failed
            status_result = "400"

        self.logger.info(f"Processing {self.plugin_name} result {status_result}")
        return status_result

# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, ScalePlugin())
