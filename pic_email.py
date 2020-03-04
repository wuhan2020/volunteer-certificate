# -*- coding: utf-8 -*-
import os
import json
from PIL import Image, ImageDraw, ImageFont
import datetime
from model import insert_people, get_number, update_status
from utils import send_email
def write_to_pic(name, email):  # 执行完这个方法后生成一个 result.png 图片 可加入email参数
    number = get_number(email)  # 用这个方法获取到编号
    date_str = datetime.datetime.strftime(datetime.datetime.now(),'%Y年%m月%d日') #获取日期
    update_status(email)  # use 参数 变为1  生成了证书
    im = Image.open("pic.jpg")
    draw = ImageDraw.Draw(im)
    font_name = ImageFont.truetype('font/1.ttf', size = 55)  # 名字的字体和字号
    font_number = ImageFont.truetype('font/1.ttf', size = 35)  # 编号的字体和字号
    setFontdate = ImageFont.truetype('font/DENG.ttf' ,size = 28)  # date字体路径
    imwidth, imheight = im.size
    font_width, font_height = draw.textsize(name, font_name)  # 获取名字的大小
    draw.text(((imwidth - font_width - font_name.getoffset(name)[0]) / 2, 470), text=name, font=font_name,
              fill=(0, 0, 0))  # 写上名字 x使用了居中
    draw.text(xy=(310, 285), text=number, font=font_number)  # 写上编号
    draw.text((464 , 900) , date_str , font = setFontdate , fill = (0 , 0 , 0))  # 写上日期
    image_file = 'result.png'
    im.save(image_file)
    update_status(email, 3)
    send_email(to_email=email,
               subject='请领取您的志愿者证书',
               content='您好，附件中有您的证书\n\n\nwuhan2020 开源社区\n\n\n社区网址：<a href="https://community.wuhan2020.org.cn/">https://community.wuhan2020.org.cn/</a>',
               attachment=[image_file]
               )
    update_status(email, 4)

def write_user():
    from faker import Faker
    fake = Faker()
    # print (fake.email())
    for i in range(0, 30):
        insert_people(name=fake.name(), email=fake.email(), token="token" + str(i))
