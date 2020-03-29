import json
import os
import unittest
from shutil import copyfile
from unittest.mock import patch

from PIL import Image

from app import app
from model import insert_people
from utils import get_email_config
from utils import get_org_config
from utils import get_smtp_url
from jobs import SendEmailJob


class UtilTest(unittest.TestCase):
    def test_getSMTP_url(self):
        smtp_url = get_smtp_url('foo@163.com')
        self.assertEqual(smtp_url, 'smtp.163.com')


class WebAPITests(unittest.TestCase):
    def test_0_send_email(self):
        with patch("yagmail.SMTP") as mock_smtp:
            SendEmailJob().send_notice_email()  # threading中raise的错误不会被catch

    def test_1_getUserInfo(self):
        client = app.test_client()
        response = client.get('/api/getUserInfo?token=token0')
        self.assertEqual(json.loads(response.data)['code'], 0)

    def test_2_submitUserInfo(self):
        client = app.test_client()
        with patch("yagmail.SMTP") as mock_smtp:
            response = client.post('/api/submitUserInfo',
                                   json={"token": "token0", "name": "new name"})
            self.assertEqual(json.loads(response.data)['code'], 0)

    def test_submitPictures(self):
        client = app.test_client()
        client.options('/api/uploadImage')
        image_file = open('config/pic.jpg', 'rb')
        response = client.post('/api/uploadImage',
                               data={'template': image_file},
                               headers={'token': '1234'})
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 0)
        image_file.close()

    def test_addUser(self):
        client = app.test_client()
        json_data = {"token": "1234", "email": ["abc@example.org", "abc.org"]}
        response = client.post('/api/addUserData', json=json_data)
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 0)
        json_data = {"token": "1234", "email": ["def2@example.org,wuhan2020030001"]}
        response = client.post('/api/addUserData', json=json_data)
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 0)

    def test_addUserRejected(self):
        client = app.test_client()
        json_data = {"token": "5678", "email": ["def@example.org"]}
        response = client.post('/api/addUserData', json=json_data)
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 1)

    def test_updateOrgConfig(self):
        client = app.test_client()
        json_data = {"token": "1234",
                     "website": "https://community.wuhan2020.org.cn/",
                     "username": "admin@example.org",
                     "password": "pswd"}
        response = client.post('/api/updateOrgConfig',
                               json=json_data,
                               headers={'Referer': 'http://example.org/admin.html'})
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 0)
        email_config = get_email_config()
        self.assertEqual(email_config["server_address"], "smtp.example.org")
        org_config = get_org_config()
        self.assertEqual(org_config["frontend_url"], 'http://example.org/index.html')

    def test_submitSendEmailRequest(self):
        client = app.test_client()
        json_data = {"token": "1234", "action": "send"}
        response = client.post('/api/email', json=json_data)
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 0)
        json_data = {"token": "4321"}
        response = client.post('/api/email', json=json_data)
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 1)


class DbOperationTests(unittest.TestCase):
    def test_insert_people(self):
        insert_people('abc@example.org', 'fake name')
        try:
            insert_people('abc@example.org', 'fake name')
        except:
            pass
    def test_insert_people_new_api(self):
        insert_people('abcd@example.org,2020030001','Yang Li')

if __name__ == '__main__':
    copyfile('config/data.json', 'data.json')
    if not os.path.isdir("images"):
        os.mkdir("images")
    if not os.path.exists('pic.jpg'):
        img = Image.new('RGB', (750, 1200))
        img.save('pic.jpg')
    unittest.main()
