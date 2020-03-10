import os
import io
import json
import logging
import utils
import re

from flask import Flask , request , render_template , send_file
from flask import Response
from tinydb import Query , TinyDB

import pic_email as wc
from model import update_status, update_name
from model import insert_people
from app_instance import app
from app_instance import logger
from jobs import SendEmailJob
from utils import get_smtp_url
send_email_job = SendEmailJob()
# 0:KEY is not right
# 1:KEY is right
# 2: Make Image& Send email sucess
# 3: Have been used
# 4:
# 5:Send wrong
def return_msg(message):
    if type(message) is dict:
        message = json.dumps(message)
    return message

def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    return False

def confirm_token(token): #finish
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.token == token)
    db.close()
    if len(res) != 0:
        return res[0]
    else:
        return False

def confirm_admin_token(token):
    orgconfig = utils.get_org_config()
    admintoken = orgconfig["admin_token"]
    if token == admintoken:
        return True
    else:
        return False

def is_token_unused(token):#确定一下Key有没有被用过
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.token == token)
    db.close()
    if res and res[0]["status"] == 1:
        return True
    else:
        return False

@app.route('/api/getUserInfo',methods = ['get', 'OPTIONS'])
def token():
    message = request.args.get('token')
    person_info = confirm_token(message)
    if person_info and person_info['status'] == 1:
        return_json = {'code': 0, 'data': person_info,'message': 'success'}
    elif person_info and person_info['status'] > 1:
        return_json = {'code': 1, 'data':'','message': 'You have submitted your information successful, please check your email'}
    else:
        return_json = {'code': 1, 'data':'','message': 'User does not exist'}
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.data = return_msg(return_json)
    return response

@app.route('/api/submitUserInfo',methods = ['POST', 'OPTIONS'])
def send_email():
    if request.method == 'POST':
        message = json.loads(request.get_data(as_text = True))
        name = message['name']
        token = message['token']
        result = confirm_token(token)  # 没有每个人唯一的Key
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    if request.method == 'OPTIONS':
        return response
    return_json = {'code': 1, 'message': '网络异常', 'data': None}
    response.data = return_msg(return_json)
    if result == False:
        return response
    email = result['email']
    if is_token_unused(token):  # 先确定下是不是志愿者列表中的token 并且是否注册过 没问题的话开始做图片
        update_status(email, 2)
        update_name(email,name)
        try:
            wc.write_to_pic(name,email,token)
            return_json = {'code': 0, 'message': 'You have submitted your information successful, the certificate is sent to you,  please check your email', 'data': None}
            response.data = return_msg(return_json)
            return response
        except Exception as e: #发送邮件或者创建图片错误 可能是邮件有问题
            logger.info(e)
            return response
    else:
        response.data = return_msg(return_json)
        return response  # Key被用过了


@app.route('/api/uploadImage', methods = ['POST', 'OPTIONS'])
def save_image():
    if request.method == 'POST':
        # get the token from the header
        token = request.headers.get('token', '')
        result = confirm_admin_token(token)  # 没有每个人唯一的Key
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    if request.method == 'OPTIONS':
        return response
    return_json = {'code': 1, 'message': '网络异常', 'data': None}
    response.data = return_msg(return_json)
    # get the image file path
    image_file = request.files.get('template', False)
    # Todo: security check of image_path
    if result == False or image_file == False:
        return response
    # overwrite pic.jpg
    basedir = os.path.dirname(__file__)
    try:
        image_file.save(os.path.join(basedir, 'pic.jpg'))
    except Exception as e:
        logger.info(e)
    return_json = {'code': 0, 'message': 'upload successfully', 'data': None}
    response.data = return_msg(return_json)
    return response    

@app.route('/api/addUserData',methods = ['POST', 'OPTIONS'])
def add_data():
    if request.method == 'POST':
        message = json.loads(request.get_data(as_text = True))
        email_list = message['email']
        token = message['token']
        result = confirm_admin_token(token)  # 没有每个人唯一的Key
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    if request.method == 'OPTIONS':
        return response
    return_json = {'code': 1, 'message': '网络异常', 'data': None}
    response.data = return_msg(return_json)
    if result == False:
        return response
    for email in email_list:
        if check_email(email) == False:
            logger.info('invalid email %s' % email)
            continue
        try:       
            insert_people(email, '')
        except KeyError:
            pass
        except Exception as e:
            logger.info(e)
    return_json = {'code': 0, 'message': 'update emails successfully', 'data': None}
    response.data = return_msg(return_json)
    return response
    
@app.route('/api/updateOrgConfig',methods = ['POST', 'OPTIONS'])
def update_config():
    if request.method == 'POST':
        message = json.loads(request.get_data(as_text = True))
        token = message["token"]
        result = confirm_admin_token(token)  # 没有每个人唯一的Key
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    if request.method == 'OPTIONS':
        return response
    return_json = {'code': 1, 'message': '网络异常', 'data': None}
    response.data = return_msg(return_json)
    if result == False:
        return response
    try:
        referer = request.headers.get('Referer', None)
        if referer is not None:
            referer = referer.replace('admin', 'index')
            message['frontend_url'] = referer
        if message.get('username'): # email admin address
            message['server_address'] = get_smtp_url(message.get('username')) # email smtp address
        orgconfig = utils.get_org_config()
        emailconfig = utils.get_email_config()
        for domain in message:
            if domain == "token" or len(str(message[domain])) == 0:
                continue
            if domain in orgconfig:
                orgconfig[domain] = message[domain]
            elif domain in emailconfig:
                emailconfig[domain] = message[domain]
        utils.update_org_config(orgconfig)
        utils.update_email_config(emailconfig)
    except Exception as e:
        logger.info(e)
    return_json = {'code': 0, 'message': 'update config successfully', 'data': None}
    response.data = return_msg(return_json)
    return response

@app.route('/api/email',methods = ['POST', 'OPTIONS'])
def email_task():
    if request.method == 'POST':
        message = json.loads(request.get_data(as_text = True))
        action = message.get('action','')
        token = message['token']
        result = confirm_admin_token(token)  # 没有每个人唯一的Key
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    if request.method == 'OPTIONS':
        return response
    return_json = {'code': 1, 'message': '网络异常', 'data': None}
    response.data = return_msg(return_json)
    if result == False:
        return response
    if action == 'send':
        send_email_job.start()
        return_json = {'code': 0, 'message': 'start send email jobs successfully', 'data': None}
    response.data = return_msg(return_json)
    return response

if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    if not os.path.isdir("images"):
        os.mkdir("images")
    host_name = '0.0.0.0'
    if os.environ.get('host'):
        host_name = os.environ['host']
    if os.environ.get('port'):
        port_name = int(os.environ['port'])
    else:
        port_name = 5000
    app.run(host=host_name, port=port_name, debug=True)
