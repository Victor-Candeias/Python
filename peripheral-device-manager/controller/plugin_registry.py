# controller/plugin_registry.py

class PluginRegistry:
    _registry = {}

    @classmethod
    def register_plugin(cls, job_type, plugin):
        cls._registry[job_type] = plugin

    @classmethod
    def get_plugin(cls, job_type):
        return cls._registry.get(job_type)