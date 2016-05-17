from globalvs import *
import os
import json

def updateConfig(config):
    configPath=os.path.join(root,"config.json")        
    f=open(configPath,"w")
    f.write(json.dumps(config,indent=4))#改写全局配置文件
    f.close()

def readConfig():#读取配置文件的信息
    try:
        configPath=os.path.join(root,"config.json")
        f=open(configPath,"r")
        config=json.loads(f.read())
        f.close()
    except:
        raise Exception("无法打开配置文件")
    return config

def readCata(database):
    try:
        cataPath=os.path.join(root,"database/"+database+"/catalog.json")
        f=open(cataPath,"r")
        cata=json.loads(f.read())
        f.close()
    except:
        raise Exception("无法找到数据库日志")
    return cata


def updateCata(database,cata):
        cataPath=os.path.join(root,"database/"+database+"/catalog.json")
        f=open(cataPath,"w")
        cata=json.dumps(cata)
        f.write(cata)
        f.close()
    

    