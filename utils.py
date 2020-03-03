import json

import yagmail


def send_email(to_email, subject, content, attachment=None):
    with open('email.json') as f:
        email_json = json.loads(f.read())
    # 链接邮箱服务器
    yag = yagmail.SMTP(user=email_json["username"],
                       password=email_json["password"],
                       host=email_json["server_address"],
                       port=email_json["smtp_port"],
                       smtp_ssl=email_json["smtp_ssl"],
                       smtp_starttls=email_json["smtp_ssl"],
                       smtp_skip_login=email_json["skip_auth"])
    # 邮箱正文
    # contents = ['您好，附件中有您的证书']
    print("send to " + to_email, 'with subject', subject)
    # 发送邮件
    yag.send(to_email, subject, content, attachment)

