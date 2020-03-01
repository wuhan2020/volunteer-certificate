# -*- coding: utf-8 -*-
import os
import json
from PIL import Image , ImageDraw , ImageFont
import random
from tinydb import TinyDB , Query ,where

#finish
def insert_db (name , email , key , number):
    db = TinyDB("data.json")
    People = Query()
    db.insert({"name": name , "email": email , "key": key , "number": number,"use":"0"})
    db.close()

#finish
def get_number (email):
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.email == email)
    db.close()
    return res[0]["number"]

#finish
def update_use(email):
    db = TinyDB("data.json")
    People = Query()
    db.update({'use':"1"} , where ("email")==email )
    db.close()

#finish
def send_email (email):  # 将result.png 发送到指定的 邮件
    email_json_file = os.path.join(os.path.dirname(__file__), 'email.json')
    if os.path.exists(email_json_file):
        email_json = json.load(open(email_json_file))
    else:
        email_json = {"username": "123@qq.com", "password": "pwd",
            "server_address": "smtp.qq.com", "smtp_port" : 465}
    import yagmail
    # 链接邮箱服务器
    yag = yagmail.SMTP(user=email_json["username"],
                       password=email_json["password"],
                       host=email_json["server_address"],
                       port=email_json["smtp_port"])
    # 邮箱正文
    contents = ['您好，附件中有您的证书']
    print("send to " + email)
    # 发送邮件
    yag.send(email , '志愿者证书' , contents , ["result.png"])

#finish
def write_to_pic (name , email):  # 执行完这个方法后生成一个 result.png 图片 可加入email参数
    number = get_number(email) #用这个方法获取到编号
    update_use(email) #use 参数 变为1  生成了证书
    im = Image.open("pic.jpg")
    draw = ImageDraw.Draw(im)
    font_name = ImageFont.truetype('font/1.ttf' , 55)  # 名字的字体和字号
    font_number = ImageFont.truetype('font/1.ttf' , size = 35)  # 编号的字体和字号
    imwidth , imheight = im.size
    font_width , font_height = draw.textsize(name , font_name)  # 获取名字的大小
    draw.text(((imwidth - font_width - font_name.getoffset(name)[0]) / 2 , 470) , text = name , font = font_name ,
        fill = (0 , 0 , 0))  # 写上名字 x使用了居中
    draw.text(xy = (310 , 285) , text = number , font = font_number)  # 写上编号
    im.save("result.png")
    send_email(email)  # 可直接发送到邮箱

def write_user():
    import faker
    from faker import Faker
    fake = Faker()
    #print (fake.email())
    for i in range(0,30):
        insert_db (fake.name() , fake.email() , "key"+str(i) , str(i))

