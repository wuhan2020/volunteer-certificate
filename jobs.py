# crontab files
import random
import time
import uuid
import threading

from tinydb import TinyDB, Query

from utils import get_email_config, send_email
from utils import get_org_config
from model import update_status_and_token
from app_instance import app
from app_instance import logger

class SendEmailJob:
    def __init__(self):
        self.is_finished = True
        self.job = None
    def start(self):
        if self.finished():
            self.job = threading.Thread(target=self.send_notice_email)
            logger.info('send email job started')
            self.job.start()
            self.is_finished = False
    def finished(self):
        if self.job is not None and self.job.is_alive() == False:
            self.is_finished = True
        return self.is_finished
    def send_notice_email(self):
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
    logger.setLevel(logging.DEBUG)
    SendEmailJob().start()
