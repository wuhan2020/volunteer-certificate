# crontab files
import random
import time
import traceback
from tinydb import TinyDB, Query

from model import update_status
from utils import send_email
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=10)
def sendEmailJob(user):
    send_email(
            to_email=user.email,
            subject='快来领取您的wuhan2020证书',
            content='<p>感谢您的辛苦付出，请点击链接领取您的志愿证书\n',
        )
    update_status(email=user.email, status=1)
    
def send_notice_email():
    try:
        """
        为当前邮箱状态为0的用户发送提醒邮件
        :return:
        """
        db = TinyDB("data.json")
        People = Query()
        target_users = db.search(People.status == 0)
        for user in target_users:
            task1=executor.submit(sendEmailJob,user)
            print(task1.result())  # 通过result来获取返回值
    except Exception as identifier:
            errorHanddler(identifier)    
        


def errorHanddler(e=Exception):
    print(str(e))
    print(repr(e))
    print(traceback.print_exc())
    print(traceback.format_exc())