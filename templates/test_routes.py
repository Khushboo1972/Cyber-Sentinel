import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_incident(self):
        response = self.app.get('/incident/1')  # Adjust based on your data
        self.assertIn(response.status_code, [200, 404])  # In case EventID 1 exists or not

    def test_404_page(self):
        response = self.app.get('/incident/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
