from globalvs import *
from parseData import *
import os
import json
import shutil
import struct
import tableFile
import bptree
import pickle


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

def deleteTable(database,table):
    path=os.path.join(root,"database/"+database+"/"+table+".tb")
    os.remove(path)

def insert(database,table,binarydata,size):#在特定的表当中插入一行，也是暂时没有考虑buffer的问题
    path=os.path.join(root,"database/"+database+"/"+table+".tb")
    tb=tableFile.BinaryRecordFile(path,size)
    tb[len(tb)]=binarydata;
    temp=len(tb)-1 
    tb.close();    
    return temp

def delete(database,table,size,positions):#删除文件当中的一行记录
    path=os.path.join(root,"database/"+database+"/"+table+".tb")
    tb=tableFile.BinaryRecordFile(path,size)
    for pos in positions:
        del tb[pos]
    
def readTable(database,table,size,pat):#读取一个表的信息
    path=os.path.join(root,"database/"+database+"/"+table+".tb")
    tb=tableFile.BinaryRecordFile(path,size)
    for row in tb:
        if row:
            yield toRecord(row, pat)

def initIndex(database,name):#初始化索引文件
    path=os.path.join(root,"database/"+database+"/"+name+".index")
    open(path,"w")

def deleteIndex(database,name):
    path=os.path.join(root,"database/"+database+"/"+name+".index")
    os.remove(path)

def updateIndex(database,name,tree):#更新索引文件
    path=os.path.join(root,"database/"+database+"/"+name+".index")
    f=open(path,"w+b")
    f.write(tree.tobinary())#更新索引文件
    f.close()

def readIndex(database,name):
    path=os.path.join(root,"database/"+database+"/"+name+".index")
    f=open(path,"r+b")
    tree=pickle.loads(f.read())#把二进制的文本转换为B树
    return tree






