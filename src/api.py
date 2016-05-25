import catalog
from fileManage import *
from parseData import *
import check
import bptree


def  findindex(scheme,column):#找到一个table当中的一列所对于的index
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

def deleteDatabase(name):
    config=catalog.readConfig()
    if name not in config["databases"]:
        raise Exception("数据库不存在")
    else:
        deleteDB(name)
        del config["databases"][name]
        catalog.updateConfig(config)

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
    if "unique" not in tableinfo["scheme"][i] and "primary" not in tableinfo["scheme"][i]:
        raise Exception("列不是unique的")#以上这一大段都是在检查完整性

    initIndex(database,name)#初始化索引文件
    tablecontents=readTable(database,table,tableinfo["size"],tableinfo["format"])

    bt=bptree.Tree()#初始化B树
    for offset,row in  enumerate(tablecontents):
        bt.insert((row[i],offset))#插入索引的节点

    updateIndex(database,name,bt)   
    tableinfo["index"][name]=if#记录下索引的名字并且其所对应的列 
    catalog.updateCata(database,cata)

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
    cata[table]["format"]=bformat
    cata[table]["size"]=size
    cata[table]["unique"]=[]

    if "primary" in restrict:
        createIndex(database,table,restrict["primary"],restrict["primary"])#如果有主键，为其创建索引
        cata[table]["index"][restrict["primary"]]=restrict["parmary"]
    if "unique" in restrict:
        for column in restrict["unique"]:
            cata[table]["unique"].append(column)

    catalog.updateCata(database,cata)
    return "表已经创建"

def dropTable(database,table):
    try:
        cata=catalog.readCata(database)
        tableinfo=cata[table]
    except:
        raise Exception("表不存在")

        for index_name in tableinfo["index"]:
            deleteIndex(database,index_name)#删除所有相关的索引

        deleteTable(database,table)
        del cata[table]
        catalog.updateCata(database,cata)

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
            inde.insert((row[i],position))
            catalog.updateIndex(database,index_name,inde)

    return "插入了1行"
        


def deleteRow(database,table,condition):
    pass

def search(database,table,condition):
    pass
    

       