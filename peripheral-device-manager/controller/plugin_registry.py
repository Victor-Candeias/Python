# controller/plugin_registry.py

class PluginRegistry:
    # Class-level variable to hold the plugin registered list
    _registry = {}

    @classmethod
    def register_plugin(cls, job_type, plugin):
        """
        Register a plugin

        Args:
            job_type (str): Type of plugin
            plugin (plugin_base:plugin): plugin to be register
        """
        cls._registry[job_type] = plugin

    @classmethod
    def get_plugin(cls, job_type):
        """
        Return the plugin by type

        Args:
            job_type (str): Plugin type

        Returns:
            plugin_base:plugin: Return the instance of the plugin
        """
        return cls._registry.get(job_type)