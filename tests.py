from app import app

import unittest


class FrackTests(unittest.TestCase):

    def test_app_create(self):
        """Confirm that application was set up correctly."""
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
