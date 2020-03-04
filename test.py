import os
from unittest.mock import patch
import unittest

import yagmail
from PIL import Image

from jobs import send_notice_email
from pic_email import write_to_pic
from app import app

class WebAPITests(unittest.TestCase):
    def test_getUserInfo(self):
        client = app.test_client()
        response = client.get('/api/getUserInfo?token=token0')
        self.assertEqual(response.status_code, 200)

class SubmitUserInfoTests(unittest.TestCase):
    def test_generate_image_and_send_email(self):
        if not os.path.exists('pic.jpeg'):
            img = Image.new('RGB', (750, 1200))
            img.save('pic.jpeg')
        with patch("yagmail.SMTP") as mock_smtp:
            write_to_pic('test name', 'muxxs@foxmail.com')

    def test_notice_email(self):
        with patch("yagmail.SMTP"):
            send_notice_email()

if __name__ == '__main__':
    unittest.main()
