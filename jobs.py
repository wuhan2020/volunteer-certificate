# crontab files
import random
import time

from tinydb import TinyDB, Query

from model import update_status
from utils import get_email_config, send_email


def send_notice_email():
    """
    为当前邮箱状态为0的用户发送提醒邮件
    :return:
    """
    db = TinyDB("data.json")
    People = Query()
    target_users = db.search(People.status == 0)
    email_config = get_email_config()
    for user in target_users[:30]:  # 这里最多需要150 * 30s来发送完毕
        send_email(
            to_email=user['email'],
            subject='快来领取您的《wuhan2020开源社区志愿者证书》',
            content='感谢您的辛苦付出，请点击链接 <a href="https://community.wuhan2020.org.cn/zh-cn/certification/index.html?token='
                    + user['token'] + '">https://community.wuhan2020.org.cn/zh-cn/certification/index.html?token='
                    + user['token'] + '</a>领取您的《志愿者证书》\nwuhan2020 开源社区\n社区网址：<a href="https://community.wuhan2020.org.cn/">https://community.wuhan2020.org.cn/</a>',
        )
        update_status(email=user['email'], status=1)
        slope = email_config["max_time"] - email_config["min_time"]
        time.sleep(email_config["min_time"] + random.random() * slope)
    db.close()

if __name__ == '__main__':
    send_notice_email()
