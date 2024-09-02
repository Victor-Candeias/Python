import unittest
from app.input_manager import InputManager
from app.input_plugins.http_plugin import HttpInputPlugin
from app.input_plugins.file_plugin import FileInputPlugin

class TestInputManager(unittest.TestCase):

    def setUp(self):
        self.manager = InputManager()
        self.http_plugin = HttpInputPlugin()
        self.file_plugin = FileInputPlugin()

    def test_register_plugin(self):
        self.manager.register_plugin(self.http_plugin)
        self.manager.register_plugin(self.file_plugin)
        self.assertIn("HTTP Input", self.manager.list_plugins())
        self.assertIn("File Input", self.manager.list_plugins())

    def test_get_plugin(self):
        self.manager.register_plugin(self.http_plugin)
        plugin = self.manager.get_plugin("HTTP Input")
        self.assertEqual(plugin.get_name(), "HTTP Input")

    def test_process_input_http_plugin(self):
        self.manager.register_plugin(self.http_plugin)
        plugin = self.manager.get_plugin("HTTP Input")
        result = plugin.process_input("http://example.com")
        self.assertEqual(result, "Processing HTTP data: http://example.com")

    def test_process_input_file_plugin(self):
        self.manager.register_plugin(self.file_plugin)
        plugin = self.manager.get_plugin("File Input")
        result = plugin.process_input("file.txt")
        self.assertEqual(result, "Processing file data: file.txt")

if __name__ == '__main__':
    unittest.main()
