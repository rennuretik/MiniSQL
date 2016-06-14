import catalog
from fileManage import *
from parseData import *
import check
import bptree
from globalvs import *


def findindex(scheme,column):  #找到一个table当中的一列所对于的index
    for index,x in enumerate(scheme, start=0):
        if column==x[0]:
            return index
    raise Exception("没有找到这样的列")    


def createDatabase(name):
    config=catalog.readConfig()
    if name in config["databases"]:
        raise Exception("数据库已经存在")
    else:
        initialDB(name)#初始化文件
        config["databases"][name]=True
        catalog.updateConfig(config)#更新全局配置
        DBs.append(name)
    return "database created"


def deleteDatabase(name):
    config=catalog.readConfig()
    if name not in config["databases"]:
        raise Exception("数据库不存在")
    else:
        deleteDB(name)
        del config["databases"][name]
        catalog.updateConfig(config)
        DBs.remove(name)
    return "database deleted"


def createIndex(database,table,column,name):
    cata=catalog.readCata(database)

    if not table in cata:
        raise Exception("表不存在")

    tableinfo=cata[table]
    
    if name in tableinfo["index"]:
        raise Exception("索引名已经存在")

    if column in tableinfo["index"]:
        raise Exception("该列的索引已经存在")

    i=findindex(tableinfo["scheme"],column)
    if "unique" not in tableinfo["scheme"][i] and "primary key" not in tableinfo["scheme"][i]:
        raise Exception("列不是unique的")#以上这一大段都是在检查完整性

    initIndex(database,name)#初始化索引文件
    tablecontents=readTable(database,table,tableinfo["size"],tableinfo["format"])

    bt=bptree.Tree()#初始化B树
    for offset,row in  enumerate(tablecontents):
        bt.insert((row[i],offset))#插入索引的节点

    updateIndex(database,name,bt)   
    tableinfo["index"][name]=i#记录下索引的名字并且其所对应的列 
    tableinfo["inindex"][str(i)]=name
    catalog.updateCata(database,cata)
    return "index created"


def findalltable(database):
    cata = catalog.readCata(database)
    for table in cata:
        yield table


def dropTable(database,table):
    try:
        cata=catalog.readCata(database)
        tableinfo=cata[table]
    except:
        raise Exception("表不存在")

    if "index" in tableinfo:#如果有索引，删除所有的索引
        for index_name in tableinfo["index"]:
            deleteIndex(database,index_name)#删除所有相关的索引

    deleteTable(database,table)
    del cata[table]
    catalog.updateCata(database,cata)
    return "table droped"


def createTable(database,table,scheme,restrict={}):
    cata=catalog.readCata(database)#暂时没有考虑buffer的问题

    if table in cata:
        raise Exception(table+"表已经存在")

    bformat,size=parseScheme(scheme)
    initTable(database,table,size)
    
    cata[table]={}
    cata[table]["scheme"]=scheme
    cata[table]["length"]=0
    cata[table]["index"]={}
    cata[table]["inindex"]={}
    cata[table]["format"]=bformat
    cata[table]["size"]=size
    cata[table]["unique"]=[]
    cata[table]["column"]=[]
    for column in scheme:
        cata[table]["column"].append(column[0])
    catalog.updateCata(database,cata)#这一行加了buffer之后可能需要删除掉

    if restrict["primary"]:
        try:
            createIndex(database,table,restrict["primary"],restrict["primary"])#如果有主键，为其创建索引
            cata[table]["index"][restrict["primary"]]=restrict["primary"]
        except Exception as e:
            dropTable(database,table)
            raise e

    if "unique" in restrict:
        for column in restrict["unique"]:
            cata[table]["unique"].append(column)

    catalog.updateCata(database,cata)
    return "table created"

def dropIndex(database,table,index):
    try:
        cata=catalog.readCata(database)
        tableinfo=cata[table]
    except:
        raise Exception("表不存在")

    if index not in tableinfo["index"]:
        raise Exception("没有改索引")

    deleteIndex(database,index)
    del tableinfo["index"][index]    
    catalog.updateCata(database,cata)
    return "index dropped"


def insertRow(database,table,row):#["xia",35]
    try:
        cata=catalog.readCata(database)
        tableinfo=cata[table]
    except:
        raise Exception("表不存在")

    def toscheme(scheme):
        for item in scheme:
            yield item[1]

    check.checkFormat(row,list(toscheme(tableinfo["scheme"])))
    tablecontents=list(readTable(database,table,tableinfo["size"],tableinfo["format"]))#这里暂时没有考虑buffer的问题
    check.checkRestrict(row,tablecontents,tableinfo)

    binaryrow=tobinary(row,tableinfo["format"])#转换成二进制
    position=insert(database,table,binaryrow,tableinfo["size"])#position是记录插入的位置
    tableinfo["length"]+=1
    catalog.updateCata(database,cata)

    if tableinfo["index"]:#如果有索引,要更新索引
        for index_name in tableinfo["index"]:
            inde=readIndex(database,index_name)
            inde.insert((row[tableinfo["index"][index_name]],position))
            updateIndex(database,index_name,inde)

    return "1 row inserted"


def deleteRow(database,table,condition=None):
    try:
        cata=catalog.readCata(database)
        tableinfo=cata[table]
    except:
        raise Exception("表不存在")

    todelete=[]#需要在文件当中删除的信息
    trees=[]
    tablecontents=list(readTable(database,table,tableinfo["size"],tableinfo["format"]))
    funcs=list(check.toClosure2(condition,tableinfo))  # 检验函数的集合
    

    def fit(record):
        for func in funcs:
            if not func(record):
                return False
        return True

    for inde in tableinfo["index"]:
        trees.append((readIndex(database,inde),tableinfo["index"][inde],inde))  # 读取出所有的索引

    for index, record in enumerate(tablecontents, start=0):
        if fit(record):  # 检查是否满足删除的条件
            todelete.append(index)
            for tree in trees:
                tree[0].delete(record[tree[1]])  # 更新索引树的信息

    for i,tree in enumerate(trees, start=0):
        updateIndex(database,tree[2],tree[0])

    deleted = 0
    for x in todelete:
        del tablecontents[x-deleted]
        deleted += 1

    delete(database, table, tableinfo["size"], todelete)
    tableinfo["length"] -= deleted
    catalog.updateCata(database, cata)
    return str(len(todelete))+" rows deleted"
   

def search(database,table,what='*',condition=None,sort=None,isreverse=False):
    try:
        cata=catalog.readCata(database)
        tableinfo=cata[table]
    except:
        raise Exception("表不存在")

    if what!=['*']:
        for column in what:
            if column not in tableinfo["column"]:
                raise Exception("没有这一列")#如果没有要查找的列报出错误

    tablecontents=list(readTable(database,table,tableinfo["size"],tableinfo["format"]))
    #读取表的信息并且读取表当中的内容
    funcs=list(check.toClosure2(condition,tableinfo))  # 检验函数的集合
    fitrecords=[]

    def fit(record):
        for func in funcs:
            if not func(record):
                return False
        return True

    for index, record in enumerate(tablecontents, start=0):
        if fit(record):  # 检查是否满足删除的条件
            fitrecords.append(record)

    if sort:
        i=findindex(tableinfo["column"],sort)
        fitrecords.sort(key=lambda x: x[i], reverse=isreverse)

    return toFormat(what, fitrecords, tableinfo["scheme"], tableinfo["column"])+str(len(fitrecords))+" row selected"
     #  返回格式化了的数据

def importExcel(database,excel,table):  #从excel当中导入
    records=list(readExcel(excel));
    for record in records:
        insertRow(database,table,record)
    return str(len(records))+" rows inserted"
    

