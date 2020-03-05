# crontab files
import random
import time
import uuid
import logging

from tinydb import TinyDB, Query

from utils import get_email_config, send_email
from utils import get_org_config
from model import update_status_and_token


def send_notice_email():
    """
    为当前邮箱状态为0的用户发送提醒邮件
    :return:
    """
    db = TinyDB("data.json")
    People = Query()
    target_users = db.search(People.status == 0)
    email_config = get_email_config()
    org_config = get_org_config()
    for user in target_users[:30]:  # 这里最多需要150 * 30s来发送完毕
        token = str(uuid.uuid1())
        content = '感谢您的辛苦付出，请点击链接 <a href="%s?token=' % org_config["frontend_url"]
        content += token + '">%s?token=' % org_config["frontend_url"]
        content += token + '</a>领取您的《志愿者证书》\n'
        content += org_config["name"]
        content += '\n网址：<a href="{0}">{0}</a>'.format(org_config["website"])

        is_successful = send_email(
            to_email=user['email'],
            subject='快来领取您的《 %s 志愿者证书》' % org_config["name"],
            content=content,
        )
        if is_successful:
            update_status_and_token(email=user['email'], status=1, token=token)
        slope = email_config["max_second"] - email_config["min_second"]
        time.sleep(email_config["min_second"] + random.random() * slope)

    db.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    send_notice_email()
