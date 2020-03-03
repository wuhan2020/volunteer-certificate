import os
from flask import Flask , request , render_template , send_file
from flask import Response
from tinydb import Query , TinyDB
import io,json
import pic_email as wc

app = Flask(__name__)
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

def confirm_token (token): #finish
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.token == token)
    if len(res) != 0:
        return res[0]
    else:
        return False


def is_token_unused(token):#确定一下Key有没有被用过
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.token == token)
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
        return_json = {'code': 1, 'data':'','message': 'you have submitted your information, please check your email'}
    else:
        return_json = {'code': 1, 'data':'','message': 'user not exist'}
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
        try:
            wc.write_to_pic(name,email)
            return_json = {'code': 0, 'message': '', 'data': None}
            response.data = return_msg(return_json)
            return response
        except : #发送邮件或者创建图片错误 可能是邮件有问题
            return return_msg("5")
    else:
        response.data = return_msg(return_json)
        return response  # Key被用过了






if __name__ == '__main__':
    host_name = '0.0.0.0'
    if os.environ.get('host'):
        host_name = os.environ['host']
    if os.environ.get('port'):
        port_name = int(os.environ['port'])
    else:
        port_name = 5000
    app.run(host=host_name, port=port_name)
