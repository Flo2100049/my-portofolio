# backend-core/tests/test_app.py
import unittest
from app import app
import os


os.environ['MONGO_URI'] = 'mongodb://localhost:27017/testdb'

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json())
        print("\nHealth check test passed!")

if __name__ == '__main__':
    unittest.main()