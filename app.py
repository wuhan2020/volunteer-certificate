import logging
from flask import Flask , request , render_template , send_file,make_response,jsonify
from tinydb import Query , TinyDB
import io,json,os
import pic_email as wc
import jobs as jobs
import traceback
#from flask_cors import CORS

app = Flask(__name__)

#CORS
#CORS(app, supports_credentials=True)

# 日志等级 #　filename: 指定日志文件名  # 存放路径
logging.basicConfig(level=logging.INFO,format='levelname:%(levelname)s filename: %(filename)s '
'outputNumber: [%(lineno)d]  thread: %(threadName)s output msg:  %(message)s'   # 日志内容
                           ' - %(asctime)s', datefmt='[%d/%b/%Y %H:%M:%S]',  # 日志时间
                    filename='./loggmsg.log') 

#根据下面的0，1，2，3，4，5，6
defaultResult_0="KEY is not right"
defaultResult_1="KEY is right"
defaultResult_2="Make Image& Send email sucess"
defaultResult_3="Have been used"
defaultResult_5="Send wrong"
defaultResult_6="Sending Notice Email"

# 0:KEY is not right
# 1:KEY is right
# 2: Make Image& Send email sucess
# 3: Have been used
# 4:
# 5:Send wrong

def errorHanddler(e=Exception,isOut=True):
    print(str(e))
    print(repr(e))
    print(traceback.print_exc())
    print(traceback.format_exc())
    logging.error(str(e))
    if isOut and isOut==True:
        return make_response(jsonify({'status':1,'message': '发生异常',"data":str(e)}) , 403)

def return_msg(status,message,data):
    return make_response(jsonify({"status":status,"message":message,"data":data}),200)

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

@app.route('/api/getUserInfo',methods = ['get', 'OPTIONS'])
def token():
    if request.method == 'POST':
        message = request.args.get('token')
        try:

            if message:
                    
                person_info = confirm_token(message)
                if person_info:
                    return return_msg(0,"获取成功",person_info)
                else:
                    return return_msg(1,"获取失败","user is not in server")
            else :
                return return_msg(1,"获取失败","data is null")
        except Exception as identifier:
                errorHanddler(identifier)

    @app.route('/api/submitUserInfo',methods = ['POST', 'OPTIONS'])
    def send_email():
        content=request.get_data(as_text = True)
        if content:
            message = json.loads(content)
            email = message['email']
            name = message['name']
            token = message['token']
            if not confirm_token(token):  # 没有每个人唯一的Key
                return return_msg(0,defaultResult_0,"")  
            if confirm_use(token):  # 先确定下是不是志愿者列表中的token 并且是否注册过 没问题的话开始做图片
                try:
                    wc.write_to_pic(name,email)
                    return return_msg(0,defaultResult_2,"")
                except : #发送邮件或者创建图片错误 可能是邮件有问题
                    return return_msg(1,defaultResult_5,"")
            else:
                return return_msg(0,defaultResult_3,"")
        else:
            return return_msg(1,"data is null","")


@app.route('/sendNoticeEmail',methods = ['GET'])
def sendNoticeEmail():
    try:
        jobs.send_notice_email()
        return return_msg(1,defaultResult_6,"")
    except Exception as identifier:
        errorHanddler(identifier)
    


if __name__ == '__main__':
    host_name = '0.0.0.0'
    if os.environ.get('host'):
        host_name = os.environ['host']
    if os.environ.get('port'):
        port_name = int(os.environ['port'])
    else:
        port_name = 5000
    app.run(host=host_name, port=port_name)
