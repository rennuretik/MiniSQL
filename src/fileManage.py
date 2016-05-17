from globalvs import *
import os
import json
import shutil


def initialDB(name):#初始化一个catalog
    path=os.path.join(root,"database/"+name)#创建数据库的目录
    os.mkdir(path)
    catalogPath=os.path.join(path,"catalog.json")
    catalog=open(catalogPath,"w")#创建数据库日志文件
    catalog.write(json.dumps({"tables": [],"index": {}}, indent=4))
    catalog.close()#初始化catalog的配置文件并初始化

def deleteDB(name):
    path=os.path.join(root,"database/"+name)
    shutil.rmtree(path)