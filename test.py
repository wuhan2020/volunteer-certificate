import os
from unittest.mock import patch
import unittest

import yagmail
from PIL import Image

from jobs import send_notice_email
from model import insert_people
from pic_email import write_to_pic
from app import app

class WebAPITests(unittest.TestCase):
    def test_getUserInfo(self):
        client = app.test_client()
        response = client.get('/api/getUserInfo?token=token0')
        self.assertEqual(response.status_code, 200)
    def test_submitUserInfo(self):
        client = app.test_client()
        response = client.post('/api/submitUserInfo', 
            json={"token":"token0", "name":"new name"})
        self.assertEqual(response.status_code, 200)
    def test_addUser(self):
        client = app.test_client()
        json_data = {"token":"admin", "email":"abc@example.org"}
        response = client.post('/api/addUserData',
            json=json_data)
        self.assertEqual(response.status_code, 200)

class SubmitUserInfoTests(unittest.TestCase):
    def test_generate_image_and_send_email(self):
        if not os.path.exists('pic.jpg'):
            img = Image.new('RGB', (750, 1200))
            img.save('pic.jpg')
        with patch("yagmail.SMTP") as mock_smtp:
            write_to_pic('test name', 'muxxs@foxmail.com')

    def test_notice_email(self):
        with patch("yagmail.SMTP"):
            send_notice_email()

class DbOperationTests(unittest.TestCase):
    def test_insert_people(self):
       insert_people('abc@example.org', 'fake name')
 
if __name__ == '__main__':
    unittest.main()
