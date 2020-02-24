from flask import Flask,request,render_template,send_file
import io
import pic_email as wc

app = Flask(__name__)

def confirm_key(key):
    return True

def confirm_email(email):
    return True

def get_time():
  return True


@app.route('/',methods=['GET'])
def hello_world():
    email = request.args.get('Email')
    name = request.args.get('name')
    key = request.args.get('key')
    if confirm_key(key)==False:  #没有每个人唯一的Key
        return ""  #404就完事了
    if email!=None and name!= None:  #是否为第一次打开页面
        if  confirm_email(email):  #先确定下是不是志愿者列表中的Email 是的话开始做图片
            #print(name,email)
            wc.write_to_pic(name)  #做图片
            wc.send_email(email) #发邮件
            with open("result.png", 'rb') as bites:
                return send_file(io.BytesIO(bites.read()), attachment_filename='line.png', mimetype='image/png') #把图片return回来
    else:  #第一次打开页面
        return render_template("index.html")

if __name__ == '__main__':
    app.run()
