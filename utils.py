import json
import os

import yagmail


def send_email(to_email, subject, content, attachment=None):
    product_file = 'email.json'
    dev_file = 'config/email.json.config'
    config_file = product_file if os.path.exists(product_file) else dev_file
    with open(config_file) as f:
        email_json = json.loads(f.read())
    # 链接邮箱服务器
    yag = yagmail.SMTP(user=email_json["username"],
                       password=email_json["password"],
                       host=email_json["server_address"],
                       port=email_json["smtp_port"],
                       smtp_ssl=email_json["smtp_ssl"],
                       )
    # 邮箱正文
    # contents = ['您好，附件中有您的证书']
    print("send to " + to_email, 'with subject', subject)
    # 发送邮件
    yag.send(to_email, subject, content, attachment)


if __name__ == '__main__':
    send_email('843213558@qq.com', 'test before push', 'It will be so luck if you receive this email', ['pic.jpg'])

