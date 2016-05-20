from globalvs import *
import os
import json
import shutil
import struct
import tableFile


def initialDB(name):#初始化一个catalog
    path=os.path.join(root,"database/"+name)#创建数据库的目录
    os.mkdir(path)
    catalogPath=os.path.join(path,"catalog.json")
    catalog=open(catalogPath,"w")#创建数据库日志文件
    catalog.write(json.dumps({}, indent=4))
    catalog.close()#初始化catalog的配置文件并初始化

def deleteDB(name):
    path=os.path.join(root,"database/"+name)
    shutil.rmtree(path)
            
def initTable(database,name,size):#scheme { a: int b: char(n) c:float }
    path=os.path.join(root,"database/"+database+"/"+name+".tb")#创建表文件对象，.tb后缀名说明其是表文件
    file=tableFile.BinaryRecordFile(path,size)
    file.close()

def insert(database,table,binarydata,size):#在特定的表当中插入一行，也是暂时没有考虑buffer的问题
    path=os.path.join(root,"database/"+database+"/"+table+".tb")
    tb=tableFile.BinaryRecordFile(path,size)
    tb[len(tb)]=binarydata;
    tb.close();    
    
def readTable(database,table,size,pat):
    path=os.path.join(root,"database/"+database+"/"+table+".tb")
    tb=tableFile.BinaryRecordFile(path,size)
    for row in tb:
        if row[0]==tableFile._OKAY:#如果记录没有被删除，生成到列表
            yield toRecord(row[1:])#生成列表，除去首个标志是否被删除的字节
        elif row[0]==tableFile._DELETED:
            continue
        else:
            raise Exception("数据错误")
        

