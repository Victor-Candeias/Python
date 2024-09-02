from app.input_plugins.base_plugin import BaseInputPlugin

class HttpInputPlugin(BaseInputPlugin):
    def get_name(self):
        return "HTTP Input"

    def process_input(self, data):
        return f"Processing HTTP data: {data}"
