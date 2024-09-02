import os
import importlib
from app.input_plugins.base_plugin import BaseInputPlugin

class InputManager:
    def __init__(self):
        self.plugins = {}
        self._register_all_plugins()

    def _register_all_plugins(self):
        """Automatically discover and register all input plugins in the plugins directory."""
        plugins_dir = os.path.join(os.path.dirname(__file__), 'input_plugins')
        for filename in os.listdir(plugins_dir):
            if filename.endswith('.py') and filename != 'base_plugin.py':
                module_name = f"app.plugins.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseInputPlugin) and attr is not BaseInputPlugin:
                        plugin_instance = attr()
                        self.register_plugin(plugin_instance)

    def register_plugin(self, plugin: BaseInputPlugin):
        """Register a new plugin."""
        plugin_name = plugin.get_name()
        if plugin_name in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' is already registered.")
        self.plugins[plugin_name] = plugin

    def get_plugin(self, plugin_name: str) -> BaseInputPlugin:
        """Retrieve a plugin by name."""
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin '{plugin_name}' not found.")
        return plugin

    def list_plugins(self):
        """List all registered plugins."""
        return list(self.plugins.keys())

    def validate_input_data(self, data: dict):
        """Validate the input data."""
        if not data or 'name' not in data or 'url' not in data:
            raise ValueError("Invalid input: 'name' and 'url' are required.")

    def process_input(self, plugin_type: str, data: dict):
        """Process input data using the specified plugin type."""
        self.validate_input_data(data)
        
        plugin = self.get_plugin(plugin_type)
        processed_data = plugin.process_input(data['url'])

        new_input = {
            "id": str(len(self.plugins) + 1),
            "name": data['name'],
            "type": data.get('type', 'stream'),
            "url": data['url'],
            "status": data.get('status', 'active'),
            "processedData": processed_data,
            "createdAt": "2024-08-21T12:34:56Z"
        }
        return new_input
