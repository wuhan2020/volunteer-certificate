import os
from unittest.mock import patch
import unittest
from shutil import copyfile

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
    def test_submitPictures(self):
        client = app.test_client()
        client.options('/api/uploadImage')
        image_file  = open('config/pic.jpg', 'rb')
        response = client.post('/api/uploadImage',
            data={'template': image_file})
        self.assertEqual(response.status_code, 200)
        image_file.close()
    def test_addUser(self):
        client = app.test_client()
        json_data = {"token":"1234", "email":"abc@example.org"}
        response = client.post('/api/addUserData',
            json=json_data)
        self.assertEqual(response.status_code, 200)
    def test_addUserRejected(self):
        client = app.test_client()
        json_data = {"token":"5678", "email":"def@example.org"}
        response = client.post('/api/addUserData',json=json_data)
        res_json = json.loads(response.data.decode('ascii'))
        self.assertEqual(res_json['code'], 0)

class SubmitUserInfoTests(unittest.TestCase):
    def test_generate_image_and_send_email(self):
        if not os.path.isdir("images"):
            os.mkdir("images")
        if not os.path.exists('pic.jpg'):
            img = Image.new('RGB', (750, 1200))
            img.save('pic.jpg')
        with patch("yagmail.SMTP") as mock_smtp:
            write_to_pic('test name', 'muxxs@foxmail.com', 'idle_token')

    def test_notice_email(self):
        with patch("yagmail.SMTP"):
            send_notice_email()

class DbOperationTests(unittest.TestCase):
    def test_insert_people(self):
        insert_people('abc@example.org', 'fake name')
        try:
            insert_people('abc@example.org', 'fake name')
        except:
            pass
 
if __name__ == '__main__':
    copyfile('config/data.json', 'data.json')
    unittest.main()
