import sys,os

import pymongo
import traceback
def errorHanddler(e=Exception):
    print(str(e))
    print(repr(e))
    print(traceback.print_exc())
    print(traceback.format_exc())
    

class PyMongoClinetUtil():
    host="127.0.0.1"
    port=27017
    
    def __init__(self,host,port):
        self.host=host
        self.port=port
        
    def getClient(self,host=host,port=port):
        
        myclient = pymongo.MongoClient(host=host,port=port)
        return myclient
    def getMyCol(self,docName):
        myclient = self.getClient()
        mydb = myclient["2019-nCov"]
        
        mycol = mydb[docName]
        return mycol
    def deleteAllData(self,docName):
        mycol=self.getMyCol(docName)
        mycol.remove()
    def deleteData(self,docName,deleteData):
        outResultData=[]
        mycol=self.getMyCol(docName)
        if isinstance (deleteData,list):
            L=len(deleteData)
            if L!=0: 
                for i1 in range(0,L):
                    target=deleteData[i1]
                    x=mycol.delete_one(target)
                    if x :
                        outResultData.append({'data':x,"code":1,"msg":"data is deleted"})
                    
                        
            else:
                outResultData.append({"result":"data is null array"})    
        else : 
            x=mycol.delete_one(deleteData)
            if x :
                #print(x)
                outResultData.append({'data':x,"code":1,"msg":"data is deleted"})
            
        return outResultData
    def insertToDb(self,inserData,docName):
        outResultData=[]
        mycol=self.getMyCol(docName)
        if isinstance (inserData,list):
            L=len(inserData)
            if L!=0: 
                for i1 in range(0,L):
                    target=inserData[i1]
                    x=mycol.find_one(target)
                    if x :
                        outResultData.append({'data':"","code":1,"msg":"data is insert into db"})
                    else :
                        x=mycol.insert_one(target)
                        if x and x.inserted_id:
                            outResultData.append({'data':x.inserted_id,"code":0,"msg":"data is insert into db"})
                        
            else:
                outResultData.append({"result":"data is null array"})    
        else : 
            x=mycol.find_one(inserData)
            if x :
                #print(x)
                outResultData.append({'data':"","code":1,"msg":"data is insert into db"})
            else :
                x=mycol.insert_one(inserData)
                if x and x.inserted_id:
                    outResultData.append({'data':x.inserted_id,"code":0,"msg":"data is insert into db"})
        return outResultData
    def fetchData(self,whichToFetch,docName):
        outResultData=[]
        
        try:
            mycol=self.getMyCol(docName)
            queryData=mycol.find_one(whichToFetch)
            if queryData!=None:
                outResultData.append(queryData)
                
            return outResultData
        except Exception as identifier:
            errorHanddler(identifier)
            return outResultData
        

    
