import json

import yagmail


def send_email(to_email, subject, content, attachment=None):
    EMAIL_INFO = json.loads(open('email.json').read())
    # 链接邮箱服务器
    yag = yagmail.SMTP(user=EMAIL_INFO['username'], password=EMAIL_INFO['password'], host=EMAIL_INFO['server_address'])
    # 邮箱正文
    # contents = ['您好，附件中有您的证书']
    print("send to " + to_email, 'with subject', subject)
    # 发送邮件
    yag.send(to_email, subject, content, attachment)

