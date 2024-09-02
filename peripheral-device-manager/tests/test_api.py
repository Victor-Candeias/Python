# tests/test_api.py
import unittest
from app import create_app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_create_output_job(self):
        response = self.app.post('/api/output_job', json={
            "machineid": "123",
            "sessionid": "abc",
            "userinfo": "user1",
            "ticket_id": "T123",
            "type_of_job": "receipt",
            "job_mode": "synchronous",
            "date": "2023-08-23"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("job_id", response.json)

if __name__ == "__main__":
    unittest.main()