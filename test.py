import os
from unittest.mock import patch
import unittest

import yagmail
from PIL import Image

from jobs import send_notice_email
from pic_email import write_to_pic


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

if __name__ == '__main__':
    unittest.main()
