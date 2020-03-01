from unittest.mock import patch
import unittest
import yagmail
from pic_email import write_to_pic

class SubmitUserInfoTests(unittest.TestCase):
    with patch("yagmail.SMTP") as mock_smtp:
        write_to_pic('test name', 'muxxs@foxmail.com')
