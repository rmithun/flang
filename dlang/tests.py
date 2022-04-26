import unittest
import json
from mock import patch

from core import app, moderator
app.testing = True


class TestCoreApi(unittest.TestCase):

    @patch('requests.post')
    def test_status_code(self, po):
        po.return_value = {'status_code': 400}
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {'paragraphs': 'my_test_url'}
            result = client.post(
                '/post',
                data=sent
            )
            # check result from server with expected data
            self.assertEqual(
                result.status_code,
                201
            )

    @patch('requests.post')
    def test_without_params(self, po):
        po.return_value = {'status_code': 400}
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {}
            result = client.post(
                '/post',
                data=sent
            )
            # check result from server with expected data
            self.assertEqual(
                result.status_code,
                400
            )

    @patch('requests.post')
    def test_moderator(self, po):
        po.return_value = {'hasFoulLanguage': False, 'status_code':200}
        with app.test_client():
            # send data as POST form to endpoint
            text = "This is a sample text\n This is again a sample"
            mod, is_foul = moderator(text)
            self.assertEqual(
                mod,
                True
            )
            self.assertEqual(
                is_foul,
                False
            )

    @patch('requests.post')
    def test_moderator_service_unavailable(self, po):
        po.return_value = {'status_code': 503}
        with app.test_client():
            # send data as POST form to endpoint
            text = "This is a sample text\n This is again a sample"
            mod, is_foul = moderator(text)
            self.assertEqual(
                mod,
                None
            )
            self.assertEqual(
                is_foul,
                False
            )

    def test_sentences(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {'fragment': 'my_test_url'}
            result = client.post(
                '/sentences',
                data=sent
            )
            # check result from server with expected data
            self.assertEqual(
                result.status_code,
                200
            )
            self.assertEqual(
                json.loads(result.text)['hasFoulLanguage'],
                False
            )

    def test_sentences_profane(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {'fragment': 'This is hell'}
            result = client.post(
                '/sentences',
                data=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.text)['hasFoulLanguage'],
                True
            )