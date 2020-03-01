from flask import Flask , request , render_template , send_file
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
        message = json.encodes(message)
    return message

def confirm_key (key): #finish
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.key == key)
    if len(res) != 0:
        return res[0]
    else:
        return False


def confirm_use(key):#确定一下Key有没有被用过
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.key == key)
    if res[0]["use"] == 0:
        return True
    else:
        return False

@app.route('/key',methods = ['post'])
def key():
    message=json.loads(request.get_data(as_text=True))
    person_info = confirm_key(message['key'])
    if person_info:
        return_json = {'code': 0, 'data': person_info,
                       'message': 'success'}
    else:
        return_json = {'code': 0, 'data':'',
                       'message': 'user not in server'}
    return return_msg(person_info)


@app.route('/send',methods = ['POST'])
def send_email():
    message = json.loads(request.get_data(as_text = True))
    email = message['email']
    name = message['name']
    key = message['key']
    if not confirm_key(key):  # 没有每个人唯一的Key
        return "0"  
    if confirm_use(key):  # 先确定下是不是志愿者列表中的key 并且是否注册过 没问题的话开始做图片
        try:
            wc.write_to_pic(name,email)
            return return_msg("2")
        except : #发送邮件或者创建图片错误 可能是邮件有问题
            return return_msg("5")
    else:
        return return_msg("3") # Key被用过了






if __name__ == '__main__':
    app.run()
