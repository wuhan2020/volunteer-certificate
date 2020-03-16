import json
import os

from flask import Response

from app_instance import app
from app_instance import logger

import yagmail

def get_smtp_url(admin_email):
    return 'smtp.' + admin_email.split('@')[-1]

def get_email_config():
    product_file = 'email.json'
    dev_file = 'config/email.json.config'
    config_file = product_file if os.path.exists(product_file) else dev_file
    with open(config_file) as f:
        email_json = json.loads(f.read())
    return email_json

def get_org_config():
    product_file = 'org.json'
    dev_file = 'config/org.json.config'
    config_file = product_file if os.path.exists(product_file) else dev_file
    with open(config_file) as f:
        org_json = json.loads(f.read())
    return org_json

def update_org_config(orgconfig):
    product_file = 'org.json'
    dev_file = 'config/org.json.config'
    config_file = product_file if os.path.exists(product_file) else dev_file
    with open(config_file, 'w') as f:
        json.dump(orgconfig, f)
       
def update_email_config(emailconfig):
    product_file = 'email.json'
    dev_file = 'config/email.json.config'
    config_file = product_file if os.path.exists(product_file) else dev_file
    with open(config_file, 'w') as f:
        json.dump(emailconfig, f)

def send_email(to_email, subject, content, attachment=None):
    email_json = get_email_config()
    # 链接邮箱服务器
    yag = yagmail.SMTP(user=email_json["username"],
                       password=email_json["password"],
                       host=email_json["server_address"],
                       port=email_json["smtp_port"],
                       smtp_ssl=email_json["smtp_ssl"],
                       smtp_starttls=email_json["smtp_ssl"] and email_json["skip_auth"],
                       smtp_skip_login=email_json["skip_auth"])
    # 邮箱正文
    # contents = ['您好，附件中有您的证书']
    logger.info("send to " + to_email + '; with subject,' + subject)
    # 发送邮件
    try:
        yag.send(to_email, subject, content, attachment)
    except Exception as e:
        logger.info('send email to %s failed; Reason:' % to_email)
        logger.info(e)
        return False
    return True


def response_json(code=0, message='success', data=None):
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    data = {
        'code': code,
        'message': message,
        'data': data
    }
    response.data = json.dumps(data)
    return response
