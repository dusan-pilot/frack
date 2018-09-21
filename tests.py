import ast
import os
import unittest
import UserDict
from app import app
from utils import generate_payload, extract_data


# added for circleci support
class EnvironmentVarGuard(UserDict.DictMixin):
    """Class to help protect the environment variable properly.  Can be used as
    a context manager."""

    def __init__(self):
        self._environ = os.environ
        self._changed = {}

    def __getitem__(self, envvar):
        return self._environ[envvar]

    def __setitem__(self, envvar, value):
        # Remember the initial value on the first access
        if envvar not in self._changed:
            self._changed[envvar] = self._environ.get(envvar)
        self._environ[envvar] = value

    def __delitem__(self, envvar):
        # Remember the initial value on the first access
        if envvar not in self._changed:
            self._changed[envvar] = self._environ.get(envvar)
        if envvar in self._environ:
            del self._environ[envvar]

    def keys(self):
        return self._environ.keys()

    def set(self, envvar, value):
        self[envvar] = value

    def unset(self, envvar):
        del self[envvar]

    def __enter__(self):
        return self

    def __exit__(self, *ignore_exc):
        for (k, v) in self._changed.items():
            if v is None:
                if k in self._environ:
                    del self._environ[k]
            else:
                self._environ[k] = v
        os.environ = self._environ


class FrackTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('SLACK_SIGNING_SECRET', 'secret')
        self.env.set('JPG', 'JpGaPpHaSh')
        self.env.set('TXT', 'TxTaPpHaSh')

        self.valid_slash_response = {
            'text': 'Your Frame app is ready!',
            'attachments': [
                {'color': '#36a64f',
                 'fallback': 'Frame app is ready!',
                 'title_link': 'do_not_test',
                 'title': 'Open frame app.'
                 }
            ]
        }

        self.verification_failed_response = {
            "text": "Server responded with: 401 Unauthorized.",
            "attachments": [
                {
                    "fallback": "Server responded with: 401 Unauthorized.",
                    "pretext": "Your request cannot be verified.",
                    "color": "#36a64f",
                    "footer": "Frack service"
                }
            ]
        }
        self.invalid_input_response = {
            "text": "Server responded with: 400 Bad Request.",
            "attachments": [
                {
                    "fallback": "Server responded with 400 Bad Request.",
                    "pretext": "Make sure your URL is not empty and not linking to unsupported resource.",  # noqa
                    "color": "#36a64f",
                    "footer": "Frack service"
                }
            ]
        }
        self.valid_txt_path = 'https://www.w3.org/TR/PNG/iso_8859-1.txt'

        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    # tests

    def test_ping_app(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_slash_valid_post_request(self):
        self.app.environ_base[
            'HTTP_X_SLACK_SIGNATURE'] = 'v0=f1ca032a11ac085b6af54404f3b2e890d81a752b51918793b2e8c9a292bd3dd3'  # noqa
        self.app.environ_base['HTTP_X_SLACK_REQUEST_TIMESTAMP'] = '1537363068'
        data = dict(user_name='tester', text=self.valid_txt_path)
        r = self.app.post('/slash', data=data, follow_redirects=True)
        actual_results = ast.literal_eval(r.get_data(as_text=True))
        actual_results['attachments'][0]['title_link'] = 'do_not_test'
        self.assertDictEqual(actual_results, self.valid_slash_response)
        self.assertEqual(r.status_code, 200)

    def test_slash_invalid_post_request_verification(self):
        self.app.environ_base['HTTP_X_SLACK_SIGNATURE'] = 'bad_signature'
        self.app.environ_base['HTTP_X_SLACK_REQUEST_TIMESTAMP'] = '1537363068'
        data = dict(user_name='tester', text='test.txt')
        r = self.app.post('/slash', data=data, follow_redirects=True)
        actual_results = ast.literal_eval(r.get_data(as_text=True))
        self.assertDictEqual(actual_results, self.verification_failed_response)
        self.assertEqual(r.status_code, 200)

    def test_slash_invalid_post_request_invalid_input(self):
        self.app.environ_base['HTTP_X_SLACK_SIGNATURE'] = 'v0=9360b99efae415568ac21cf371cf7cf363fd7d548dc3e458704eb5af2923fa4b'  # noqa
        self.app.environ_base['HTTP_X_SLACK_REQUEST_TIMESTAMP'] = '1537363068'
        data = dict(user_name='tester', text='')
        r = self.app.post('/slash', data=data, follow_redirects=True)
        actual_results = ast.literal_eval(r.get_data(as_text=True))
        self.assertDictEqual(actual_results, self.invalid_input_response)
        self.assertEqual(r.status_code, 200)

    def test_extract_data(self):
        notepad_app_hash = "TxTaPpHaSh"
        self.assertEqual(extract_data(None), None)
        self.assertEqual(extract_data(""), None)
        self.assertEqual(extract_data("bad_input"), None)
        self.assertEqual(
            extract_data("https://www.w3.org/TR/PNG/iso_8859-1.txt"),
            notepad_app_hash)

    def test__generate_payload(self):
        frame_app_url_sample = "https://frack?url=p.jpg&app_hash=2p9wDg1G"

        expected_payload = {
            'text': 'Your Frame app is ready!',
            'attachments': [
                {
                    'fallback': 'Frame app is ready!',
                    'color': '#36a64f',
                    'title': 'Open frame app.',
                    'title_link': frame_app_url_sample
                }
            ]
        }

        actual_payload = generate_payload(frame_app_url_sample)
        self.assertEqual(expected_payload, actual_payload)


if __name__ == '__main__':
    unittest.main()
