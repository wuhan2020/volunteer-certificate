# crontab files
import random
import time

from tinydb import TinyDB, Query

from model import update_status
from utils import send_email


def send_notice_email():
    """
    为当前邮箱状态为0的用户发送提醒邮件
    :return:
    """
    db = TinyDB("data.json")
    People = Query()
    target_users = db.search(People.status == 0)
    for user in target_users:
        send_email(
            to_email=user['email'],
            subject='快来领取您的wuhan2020开源社区志愿者证书',
            content='感谢您的辛苦付出，请点击链接https://community.wuhan2020.org.cn/volunteer/update-name.html?token='+user['token']+'领取您的《志愿者证书》(一个月内有效)\n',
        )
        update_status(email=user['email'], status=1)
        time.sleep(random.random() * 10)
    db.close()
