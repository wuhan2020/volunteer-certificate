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


def confirm_use(token):#确定一下Key有没有被用过
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.token == token)
    if res[0]["status"] == 0:
        return True
    else:
        return False

@app.route('/token',methods = ['post'])
def token():
    message=json.loads(request.get_data(as_text=True))
    person_info = confirm_token(message['token'])
    if person_info:
        return_json = {'code': 0, 'data': person_info,
                       'message': 'success'}
    else:
        return_json = {'code': 0, 'data':'',
                       'message': 'user not in server'}
    return return_msg(person_info)


@app.route('/api/submitUserInfo',methods = ['POST'])
def send_email():
    message = json.loads(request.get_data(as_text = True))
    name = message['name']
    token = message['token']
    result = confirm_token(token)  # 没有每个人唯一的Key
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    return_json = {'code': 1, 'message': '网络异常', 'data': None}
    response.data = return_msg(return_json)
    if result == False:
        return response
    email = result['email']
    if confirm_use(token):  # 先确定下是不是志愿者列表中的token 并且是否注册过 没问题的话开始做图片
        try:
            wc.write_to_pic(name,email)
            return_json = {'code': 0, 'message': '', 'data': None}
            response.data = return_msg(return_json)
            return response
        except : #发送邮件或者创建图片错误 可能是邮件有问题
            return return_msg("5")
    else:
        return return_msg("3") # Key被用过了






if __name__ == '__main__':
    app.run()
