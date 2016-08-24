from uploader import app
import unittest
import json
from StringIO import StringIO


class UploadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_empty_file_upload(self):
        result = self.app.post('/')
        self.assertEqual(json.loads(result.data).get('error', None), 'No file part')
        self.assertEqual(result.status_code, 412)

    def test_wrong_extension_file_upload(self):
        result = self.app.post('/', data=dict(file=(StringIO('test'), 'test.jpg')),
                               content_type='multipart/form-data')
        self.assertEqual(json.loads(result.data).get('error', None), 'bad extension')
        self.assertEqual(result.status_code, 412)

    def test_csv_extension_file_upload(self):
        result = self.app.post('/', data=dict(file=(StringIO('test'), 'test.csv')),
                               content_type='multipart/form-data')
        self.assertEqual(result.status_code, 202)

    def test_bad_url_download_file_upload(self):
        result = self.app.post('/', data=dict(submit="Download", url='test'),
                               content_type='multipart/form-data')
        self.assertEqual(json.loads(result.data).get('error', None), 'No csv file')
        self.assertEqual(result.status_code, 412)

    def test_empty_url_download_file_upload(self):
        result = self.app.post('/', data=dict(submit="Download"),
                               content_type='multipart/form-data')
        self.assertEqual(json.loads(result.data).get('error', None), 'No url provided')
        self.assertEqual(result.status_code, 412)

    def test_not_being_able_to_download_remote_file(self):
        result = self.app.post('/', data=dict(submit="Download", url='test.csv'),
                               content_type='multipart/form-data')
        self.assertEqual(json.loads(result.data).get('error', None), 'cannot download by url')
        self.assertEqual(result.status_code, 412)

if __name__ == '__main__':
    unittest.main()
