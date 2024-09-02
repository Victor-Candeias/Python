import unittest
from app import create_app, input_manager
from flask import json

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_create_output_job(self):
        """Test creating a new output job."""
        response = self.client.post(
            '/output-jobs',
            data=json.dumps({
                "name": "Test Job",
                "source": "camera1",
                "destination": "output1"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Test Job')

    def test_create_output_job_invalid(self):
        """Test creating a new output job with invalid data."""
        response = self.client.post(
            '/output-jobs',
            data=json.dumps({
                "source": "camera1",
                "destination": "output1"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_input_with_plugin(self):
        """Test creating an input with a specified plugin."""
        plugin_type = "HTTP Input"
        response = self.client.post(
            f'/inputs/{plugin_type}',
            data=json.dumps({
                "name": "Test Input",
                "url": "http://example.com/stream",
                "type": "stream",
                "status": "active"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], "Test Input")
        self.assertEqual(data['processedData'], "Processing HTTP data: http://example.com/stream")

    def test_create_input_invalid_plugin(self):
        """Test creating an input with an invalid plugin type."""
        plugin_type = "Invalid Plugin"
        response = self.client.post(
            f'/inputs/{plugin_type}',
            data=json.dumps({
                "name": "Test Input",
                "url": "http://example.com/stream"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_list_devices(self):
        """Test listing all devices."""
        response = self.client.get('/devices')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertGreater(len(data), 0)
    
    def test_list_plugins(self):
        """Test listing all available plugins."""
        response = self.client.get('/plugins')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
