import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import traceback
import qrcode
import os,sys

from PIL import Image,ImageDraw,ImageFont
import matplotlib.pyplot as plt
from bson.objectid import ObjectId
from concurrent.futures import ThreadPoolExecutor
class MailConfig(object):
    mail_host = '',
    mail_user = '',
    mail_pass = '',
    mail_port = 0
    

executor = ThreadPoolExecutor(max_workers=10)


class PIC_Util():
    curpath_=os.path.dirname(__file__)
    curpath=os.path.dirname(curpath_)
    curpath1=os.path.abspath(curpath)
    
    curpath2=os.path.abspath(os.path.dirname(curpath1))
    logoImgPath=os.path.join(curpath2,"bg.jpg")
    imgPath=""
    def getNuber(self,UserId):
        return "wuhan20200000"+UserId #返回编号的方法

    def createIdCard(self,name,email,UserId):
        print(self.logoImgPath)
        # 添加logo，打开logo照片
        number=self.getNuber(UserId)
        bg = Image.open(self.logoImgPath)
        draw = ImageDraw.Draw(bg)
        fontPath=os.path.join(self.curpath_+"\\font\\","1.ttf")
        print("fontPath:"+fontPath)
        
        font_name = ImageFont.truetype(fontPath,size=55) # 名字的字体和字号
        font_number=ImageFont.truetype(fontPath,size=35) # 编号的字体和字号
        imwidth, imheight = bg.size
        font_width, font_height = draw.textsize(name, font_name) # 获取名字的大小
        draw.text(((imwidth - font_width - font_name.getoffset(name)[0]) / 2, 470), text=name , font=font_name, fill=(0, 0, 0)) # 写上名字 x使用了居中
        draw.text(xy=(310,285),text=number,font=font_number) # 写上编号
        
        # 保存img
        imgFolder=self.curpath2+"\\IdCard\\"
        if not os.access(imgFolder, os.F_OK):
            os.makedirs(imgFolder)
        
        imgPath=os.path.join(self.curpath2+"\\IdCard\\",name+".jpg")
        self.imgPath=imgPath
        print(imgPath)
        if os.access(imgPath, os.F_OK):
            os.remove(imgPath)
        bg.save(imgPath)
        bg.close()
        return bg

class Mail_Util():
    curpath=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    curpath1=os.path.abspath(os.path.dirname(curpath))
    
    Config_=MailConfig()
    def __init__(self,Config=MailConfig):
        self.Config_=Config
        
        print(Config) 
    
            
    def sendEmailTask(self,sendToAddress,SendUserName,ImageFilePath):
        # 第三方 SMTP 服务
    
        print(self.curpath)
        
        try:
            sender = self.Config_.mail_user
            receivers = [sendToAddress]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
            message = MIMEMultipart()
            
            message['From'] = Header("菜鸟教程", 'utf-8')
            message['To'] =  Header("测试", 'utf-8')
            
            subject = '志愿者证书'
            message['Subject'] = Header(subject, 'utf-8')
            ImageFilePath_=""
            if ImageFilePath==None:
                
                ImageFilePath_=os.path.join(self.curpath2+"\\IdCard\\",SendUserName+".jpg")
            else:
                if len(ImageFilePath)!=0:    
                    ImageFilePath_=ImageFilePath
                else:
                    ImageFilePath_=os.path.join(self.curpath2+"\\IdCard\\",SendUserName+".jpg")
            
            message.attach(MIMEText("您好，附件中有您的证书",_subtype='plain',_charset='utf-8'))      
            with open(ImageFilePath_,'rb') as picAtt:
                msgImg = MIMEImage(picAtt.read())
                msgImg.add_header('Content-Disposition', 'attachment', filename='你.jpg')
                #msgImg.add_header('Content-ID', '<0>')
                #msgImg.add_header('X-Attachment-Id', '0')
                message.attach(msgImg)
                
                
            
            
            
            smtpObj = smtplib.SMTP_SSL(self.Config_.mail_host,self.Config_.mail_port)
            
            smtpObj.login(self.Config_.mail_user,self.Config_.mail_pass)
            
            
            
            
            
            smtpObj.sendmail(sender, receivers, message.as_string())
            print ("邮件发送成功")
        except smtplib.SMTPException as ex:
            errorHanddler(ex)
            print ("Error: 无法发送邮件")
        finally:
            smtpObj.close()
    def doSendEmailJob(self,sendToAddress,SendUserName,ImageFilePath):
        try:
            task1=executor.submit(self.sendEmailTask,sendToAddress,SendUserName,ImageFilePath)
            print(task1.result())  # 通过result来获取返回值
        except Exception as identifier:
            errorHanddler(identifier)        
def errorHanddler(e=Exception):
    print(str(e))
    print(repr(e))
    print(traceback.print_exc())
    print(traceback.format_exc())


