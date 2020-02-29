import configparser
import os
class myconf(configparser.ConfigParser):  
        def __init__(self,defaults=None):  
            configparser.ConfigParser.__init__(self,defaults=None)  
        def optionxform(self, optionstr):  
            return optionstr

class ConfigTools():
    
    
    
#用os模块来读取
    
    def getConf(self):
        conf=myconf() 
        return conf
    def getConfigMap(self,cfgpath):
        ConfigMap={}
        print(cfgpath)
        conf=self.getConf()
        conf.read(cfgpath,encoding='UTF-8')
        for  i in conf.sections():
            #print (conf.options(i))
            ConfigMap_={}
            for option in  conf.options(i):
                #print (option,conf.get(i,option))   
                ConfigMap_[option]=conf.get(i,option)
            ConfigMap[i]= ConfigMap_   
        return ConfigMap    
if __name__ == '__main__':  
    curpath=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(curpath)
    cfgpath=os.path.join(curpath,"config.ini")  #读取到本机的配置文件
    ConfigTools=ConfigTools()
    
    print(ConfigTools.getConfigMap(cfgpath))