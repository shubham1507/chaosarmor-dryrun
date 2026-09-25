import unittest
from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flask app is running.', response.data)

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'ok'})

    def test_info(self):
        self.assertEqual(self.client.get('/api/info').json['name'], 'chaosarmor-python-demo')

    def test_unknown_route(self):
        self.assertEqual(self.client.get('/missing').status_code, 404)


if __name__ == '__main__':
    unittest.main()
