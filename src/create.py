import json
import os,sys
from globalvs import *
from Myfunc.fileManger import *

def createDatabase(name):
    configPath=os.path.join(root,"config.json")
    f=open(configPath,"r")
    config=json.loads(f.read())#得到现在已经有了的数据库
    f.close()
    if name in config["databases"]:
        raise Exception("数据库已经存在")
    else:
        path=os.path.join(root,"database\\"+name)
        createDir(path)
        catalogPath=os.path.join(path,"catalog.json")
        catalog=open(catalogPath,"w")#创建数据库日志文件
        catalog.write(json.dumps({"tables": [],"index": {}}, indent=4))
        catalog.close()#初始化catalog的配置文件并初始化

        config["databases"].append(name)
        f=open(configPath,"w")
        f.write(json.dumps(config,indent=4))#改写全局配置文件
        f.close();#关闭全局配置文件





