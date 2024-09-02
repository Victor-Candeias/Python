from app.input_plugins.base_plugin import BaseInputPlugin

class FileInputPlugin(BaseInputPlugin):
    def get_name(self):
        return "File Input"

    def process_input(self, data):
        return f"Processing file data: {data}"
