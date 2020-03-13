# -*- coding: utf-8 -*-
import os
import json
import datetime

from PIL import Image, ImageDraw, ImageFont

from model import get_number, update_status
from utils import send_email, get_org_config

def write_to_pic(name, email, token):  # 执行完这个方法后生成一个 result.png 图片 可加入email参数
    number = get_number(email)  # 用这个方法获取到编号
    date_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y{0}%m{1}%d{2}').format(*'年月日')  # 获取日期
    update_status(email)  # use 参数 变为1  生成了证书
    org_config = get_org_config()    
    im = Image.open("pic.jpg")
    draw = ImageDraw.Draw(im)
    font_name = ImageFont.truetype('font/1.ttf', size = 55)  # 名字的字体和字号
    font_number = ImageFont.truetype('font/2.ttf', size = 35)  # 编号的字体和字号
    setFontdate = ImageFont.truetype('font/DENG.TTF' ,size = 28)  # date字体路径
    imwidth, imheight = im.size
    font_width, font_height = draw.textsize(name, font_name)  # 获取名字的大小
    horizontal_offset = (font_width - font_name.getoffset(name)[0]) / 2
    draw.text((org_config["name_horizontal_pos"] - horizontal_offset,
              org_config['name_vertical_pos']),
              text=name, font=font_name,
              fill=(0, 0, 0))  # 写上名字 x使用了居中
    if org_config["serial_number_horizontal_pos"] > 0:
        draw.text(xy=(org_config["serial_number_horizontal_pos"],
                    org_config["serial_number_vertical_pos"]),
                text=number, font=font_number)  # 写上编号
    if org_config["date_horizontal_pos"] > 0:
        draw.text((org_config["date_horizontal_pos"],
                org_config["date_vertical_pos"]),
                date_str , font = setFontdate , fill = (0 , 0 , 0))  # 写上日期
    image_file = 'images/%s.png' % token
    im.save(image_file)
    update_status(email, 3)
    content = '您好，附件中有您的证书\n\n\n'
    content += org_config["name"]
    content += '\n\n\n网址：<a href="{0}">{0}</a>'.format(org_config["website"])
    send_email(to_email=email,
               subject='请领取您的志愿者证书',
               content=content,
               attachment=[image_file]
               )
    update_status(email, 4)

