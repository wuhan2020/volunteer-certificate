import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import traceback
import qrcode
import os,sys

from PIL import Image
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
    curpath=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    curpath=os.path.abspath(os.path.dirname(curpath))
    logoImgPath=os.path.join(curpath,"logo.png")
    imgPath=""
    def createIdCard(self,name,email):
        print(self.logoImgPath)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=4,
        )

        # 添加数据
        data="志愿者名称："+name+",邮箱地址："+email
        qr.add_data(data)
        # 填充数据
        qr.make(fit=True)
        # 生成图片
        img = qr.make_image(fill_color="green", back_color="white")

        # 添加logo，打开logo照片
        
        icon = Image.open(self.logoImgPath)
        # 获取图片的宽高
        img_w, img_h = img.size
        # 参数设置logo的大小
        factor = 6
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        # 重新设置logo的尺寸
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        # 得到画图的x，y坐标，居中显示
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        # 黏贴logo照
        img.paste(icon, (w, h), mask=None)
        # 终端显示图片
        #plt.imshow(img)
        #plt.show()
        # 保存img
        imgFolder=self.curpath+"\\IdCard\\"
        if not os.access(imgFolder, os.F_OK):
            os.makedirs(imgFolder)
        
        imgPath=os.path.join(self.curpath+"\\IdCard\\",name+".jpg")
        self.imgPath=imgPath
        print(imgPath)
        if os.access(imgPath, os.F_OK):
            os.remove(imgPath)
        img.save(imgPath)
        img.close()
        return img

class Mail_Util():
    curpath=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    curpath=os.path.abspath(os.path.dirname(curpath))
    curpath=os.path.abspath(os.path.dirname(curpath))
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
            
            subject = 'Python SMTP 邮件测试'
            message['Subject'] = Header(subject, 'utf-8')
            ImageFilePath_=""
            if ImageFilePath==None:
                
                ImageFilePath_=os.path.join(self.curpath+"\\IdCard\\",SendUserName+".jpg")
            else:
                if len(ImageFilePath)!=0:    
                    ImageFilePath_=ImageFilePath
                else:
                    ImageFilePath_=os.path.join(self.curpath+"\\IdCard\\",SendUserName+".jpg")
                    
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

if __name__ == "__main__":
    Config=MailConfig()   
    Config.mail_host='smtp.qq.com'
    Config.mail_pass='yeghnkumvdzpbdgg'
    Config.mail_user='nwljy@vip.qq.com'
    Config.mail_port=465
    PIC_Util=PIC_Util()
    PIC_Util.createIdCard("nwljy","nwljy111@yeah.net")
    Mail_Util=Mail_Util(Config=Config)
    Mail_Util.doSendEmailJob("nwljy111@yeah.net","nwljy",None)