

import json
import hashlib
import chardet
import traceback
from datetime import datetime, timedelta
import sys,os
import qrcode
import matplotlib.pyplot as plt
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename # 使用这个是为了确保filename是安全的
from model.package_tools import PyMongoClinetUtil
from concurrent.futures import ThreadPoolExecutor
from ConifgTools import ConfigTools
screct_key = "test"
from model.package_tools.Mail_PIC_Util import PIC_Util,Mail_Util,MailConfig
import jwt
from jwt import PyJWTError
from flask import Flask,session,request,make_response,render_template, redirect, url_for,Response,jsonify
from flask_cors import CORS
from PIL import Image
PyMongoClinetUtil_=None

import base64
#test flask server
# 可以加个判断
curpath=os.path.dirname(__file__)
print(curpath)
cfgpath=os.path.join(curpath,"ServerConfig.ini")  #读取到本机的配置文件
ConfigTools=ConfigTools()
print(cfgpath)
confMap={}
confMap=ConfigTools.getConfigMap(cfgpath)
ServerConfigMap={}
client=None
MONGODB_HOST=""
MONGODB_PORT=""
MONGODB_DB=""
userDocName='User'
roleDocName='Role'
userImageDocName='UserImage'
executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞

db=None
if confMap!=None and len(confMap)!=0:
    ServerConfigMap=confMap.get('ServerConfig',None)
    print(ServerConfigMap)
    if ServerConfigMap!=None and len(ServerConfigMap)!=0:
        MongoClientIp=ServerConfigMap.get('MongoClientIp','127.0.0.1')
        MongoClientPort=int(ServerConfigMap.get('MongoClientPort',27017))
        print(MongoClientIp,MongoClientPort)
        PyMongoClinetUtil_=PyMongoClinetUtil(MongoClientIp,MongoClientPort)
        
        
#Config_=Config()


def errorHanddler(e=Exception,isOut=True):
    print(str(e))
    print(repr(e))
    print(traceback.print_exc())
    print(traceback.format_exc())
    if isOut and isOut==True:
        return make_response(jsonify({'code':1,'message': '发生异常',"data":str(e)}) , 403)
port=5000
host='127.0.0.1'
app = Flask(__name__,static_url_path='/static/',template_folder='templates')

CORS(app, supports_credentials=True)



class Config(object):
    SECRET_KEY = 'abc',
    DEBUG = True,
    MONGODB_DB = '',
    MONGODB_HOST = '',
    MONGODB_PORT = ''

@app.route('/api/addUserData',methods=['POST'])
def addUserData():
    content = request.get_json(silent=True)
    if content!=None and len(content)!=0:
        UserInsertData=content.get('UserInsertData',None)

        token = content.get('Token',None)
    if  token!=None and len(token)!=0:
        userData = None
                #需要解析的 jwt密钥使用和加密时相同的算法
                # 如果 jwt 被篡改过; 或者算法不正确; 如果设置有效时间, 过了有效期; 或者密钥不相同; 都会抛出相应的异常
        try:
            userData = jwt.decode(token, screct_key, algorithms=['HS256'])
                
                
        except Exception as e:
            print(e)
            return make_response(jsonify({'code':1,'message': str(e)}) , 500)
                # 解析出来的就是 payload 内的数据
            
    print("userData:"+str(userData))
    if userData:
        Role=userData.get('Role',None)
        UserId=userData.get('UserId',None)
        if Role:
            if Role=='Admin':
                data=PyMongoClinetUtil_.fetchData({'_id':UserId,'Role':Role},roleDocName)
                if data and len(data)!=0:
                    if UserInsertData and len(UserInsertData)!=0:
                        UserInsertData_={}
                        UserInsertData_=UserInsertData
                        UserData=[]
                        UserRoleData=[]
                        UserData=UserInsertData_.get("UserData",None)
                        UserRoleData=UserInsertData_.get("UserRoleData",None)
                        outResultData=PyMongoClinetUtil_.insertToDb(UserData,userDocName)
                        outResultData=PyMongoClinetUtil_.insertToDb(UserRoleData,UserRoleData)
                        if outResultData:
                            if len(outResultData)>0 and outResultData[0]['code']!=None and outResultData[0]['code']==0:
                                return make_response(jsonify({'code':0,'message': 'success','data':""}) , 200)
                            else:
                                return make_response(jsonify({'code':1,'message': 'error','data':""}) , 200)
                    else: 
                        return make_response(jsonify({'code':1,'message': 'insertdata is null','data':""}) , 200)
                else:
                    return make_response(jsonify({'code':1,'message': 'user data is wrong','data':""}) , 200)     
            else:
                return make_response(jsonify({'code':1,'message': 'user Role is wrong','data':""}) , 200) 

@app.route('/api/getImage',methods=['POST'])   
def getImage():
    content = request.get_json(silent=True)
    if content!=None and len(content)!=0:
        ImageId=content.get('ImageId',None)
        email=content.get('Email',None)
        name=content.get('Name',None)
        token = content.get('Token',None)
            
        if ImageId!=None and len(str(ImageId))!=0 and email!=None and len(str(email))!=0 and name!=None and len(str(name))!=0 and token!=None and len(token)!=0 :
            userData = None
                #需要解析的 jwt密钥使用和加密时相同的算法
                # 如果 jwt 被篡改过; 或者算法不正确; 如果设置有效时间, 过了有效期; 或者密钥不相同; 都会抛出相应的异常
            try:
                userData = jwt.decode(token, screct_key, algorithms=['HS256'])
                
                
            except Exception as e:
                print(e)
                return make_response(jsonify({'code':1,'message': str(e)}) , 500)
                # 解析出来的就是 payload 内的数据
            
            print("userData:"+str(userData))
            imageId_=ObjectId(ImageId)
            outResultData=PyMongoClinetUtil_.fetchData({'email':email,'name':name,"IsCreate":"1","_id":imageId_},userImageDocName)
            print(outResultData)
            if outResultData and len(outResultData)!=0:
                if outResultData[0]['ImgPath']!=None and len(str(outResultData[0]['ImgPath']))!=0:
                    
                    with open(str(outResultData[0]['ImgPath']), 'rb') as f:
                        base64_data = base64.b64encode(f.read())
                        s = base64_data.decode()
                        imageBegin='data:image/jpeg;base64,'
                        return make_response(jsonify({'code':0,'message': 'success','data':imageBegin+s}) , 200)
                else:
                    return make_response(jsonify({'code':1,'message': 'error','data':""}) , 200)    
            else:
                return make_response(jsonify({'code':1,'message': 'error','data':""}) , 200)
        else:   
            return make_response(jsonify({'code':1,'message': 'type_error',"data":""}) , 500)


@app.route('/api/createIdCard',methods=['POST'])
def createIdCard():
    # 获取json格式的body，返回直接就是dict类型
    content = request.get_json(silent=True)
    if content!=None and len(content)!=0:
        UserEmail = content.get('Email',None)
        UserName = content.get('Name',None)
        token = content.get('Token',None)
        
        if UserEmail!=None and len(str(UserEmail))!=0 and UserName!=None and len(str(UserName))!=0 and token!=None and len(token)!=0 :
            #查有此人
            userData = None
            #需要解析的 jwt密钥使用和加密时相同的算法
            # 如果 jwt 被篡改过; 或者算法不正确; 如果设置有效时间, 过了有效期; 或者密钥不相同; 都会抛出相应的异常
            try:
                userData = jwt.decode(token, screct_key, algorithms=['HS256'])
            except Exception as e:
                print(e)
                return make_response(jsonify({'code':1,'message': str(e)}) , 500)
            # 解析出来的就是 payload 内的数据
            print(userData)
            data=PyMongoClinetUtil_.fetchData({'email':UserEmail,'name':UserName},userDocName)
            if data:
                data=PyMongoClinetUtil_.fetchData({'email':UserEmail,'name':UserName,"IsCreate":"1"},userImageDocName)
                if data and len(data)!=0:
                    print(data)
                    return make_response(jsonify({'code':1,'message': 'user create yet'}) , 500)
                else :
                    UserId=userData.get('UserId',"1")
                    PIC_Util_=PIC_Util()
                    PIC_Util_.createIdCard(UserName,UserEmail,UserId)
                    outResultData=[]
                    outResultData=PyMongoClinetUtil_.insertToDb({'email':UserEmail,'name':UserName,"IsCreate":"1","ImgPath":PIC_Util_.imgPath},userImageDocName)
                    if len(outResultData)>0 and outResultData[0]['code']!=None and outResultData[0]['code']==0:
                        imageId=outResultData[0]['data']
                        print(str(imageId))
                        MailConfig_=MailConfig()
                        MailConfig_.mail_host=ServerConfigMap.get('mail_host',None)
                        MailConfig_.mail_pass=ServerConfigMap.get('mail_pass',None)
                        MailConfig_.mail_user=ServerConfigMap.get('mail_user',None)
                        MailConfig_.mail_port=ServerConfigMap.get('mail_port',None)
                        Mail_Util_=Mail_Util(Config=MailConfig_)
                        Mail_Util_.doSendEmailJob(UserEmail,UserName,None)
                        return make_response(jsonify({"code":0,"message": "sucess","data":str(imageId)}) , 200)
                    
            else :
                return make_response(jsonify({'code':1,'message': 'user is not in server',"data":""}) , 500)
                
        else : 
            return make_response(jsonify({'code':1,'message': 'type_error',"data":""}) , 500)
    
    else : 
            return make_response(jsonify({'code':1,'message': "data is null","data":""}) , 500)

        




def startServer(host='127.0.0.1',port=5000):
    app.run(host=host,port=port)

@app.route('/api/getManagerToken/<UserName>/<UserEmail>/<Userpass>',methods=['GET'])
def getManagerToken(UserName,UserEmail,Userpass):
    payload = {  # jwt设置过期时间的本质 就是在payload中 设置exp字段, 值要求为格林尼治时间
        "Role":"Admin",      
        "UserId": 1,
        'exp': datetime.utcnow() + timedelta(seconds=30*60)
    }

    
    # 生成token
    
    userData=PyMongoClinetUtil_.fetchData({'email':UserEmail,'name':UserName,"Password":Userpass},userDocName)
    roleData=PyMongoClinetUtil_.fetchData({'email':UserEmail,'name':UserName},userDocName)
    if userData and len(userData)!=0 and roleData and len(roleData)!=0:
        print(userData)
        payload['UserId']=str(userData['_id'])
        payload['Role']=str(roleData['Role'])
        token = jwt.encode(payload, key=screct_key, algorithm='HS256')
        return make_response(jsonify({"code":0,"message": "sucess","data":token}) , 200)
    else:
        return make_response(jsonify({"code":1,"message": "user not in server","data":""}) , 200)


    
@app.route('/api/getUserToken/<UserName>/<UserEmail>',methods=['GET'])
def getUserToken(UserName,UserEmail):
    payload = {  # jwt设置过期时间的本质 就是在payload中 设置exp字段, 值要求为格林尼治时间
        "Role":"User",      
        "user_id": 1,
        'exp': datetime.utcnow() + timedelta(seconds=30*60)
    }

    
    # 生成token
    
    data=PyMongoClinetUtil_.fetchData({'email':UserEmail,'name':UserName},userDocName)
    if data and len(data)!=0:
        print(data)
        payload['user_id']=str(data[0]['_id'])
        
        token = jwt.encode(payload, key=screct_key, algorithm='HS256')
        return make_response(jsonify({"code":0,"message": "sucess","data":token}) , 200)
    else:
        return make_response(jsonify({"code":1,"message": "user not in server","data":""}) , 200)
if __name__ == '__main__':
    
    
            host=ServerConfigMap.get('ServerHost','127.0.0.1')
            port=int(ServerConfigMap.get('ServerPort',8080))
            
            print(ServerConfigMap)
            Config_=Config()
            print(Config_)
            Config_.MONGODB_DB=MONGODB_DB
            Config_.MONGODB_HOST=MONGODB_HOST
            Config_.MONGODB_PORT=MONGODB_PORT
            app.config.from_object(Config_)
            
            PyMongoClinetUtil_.deleteAllData(userDocName)
            PyMongoClinetUtil_.deleteAllData(roleDocName)
            PyMongoClinetUtil_.deleteAllData(userImageDocName)
            print(PyMongoClinetUtil_.insertToDb([{"email":"nwljy111@yeah.net","name":"nwljy","Role":"Admin"}],roleDocName))
            print(PyMongoClinetUtil_.insertToDb([{"email":"nwljy111@yeah.net","name":"nwljy","Role":"Admin"}],roleDocName))

            print(PyMongoClinetUtil_.insertToDb([{"email":"pengcc981@gmail.com","name":"pengcc981","Password":"8888"}],userDocName))
            print(PyMongoClinetUtil_.insertToDb([{"email":"muxxs@foxmail.com","name":"muxxs","Password":"8888"}],userDocName))
            
            startServer(host=host,port=port)
            
    
