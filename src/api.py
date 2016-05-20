import catalog
from fileManage import *
from parseData import *
import check

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
    pass

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

    if "primary" in restrict:
        createIndex(database,table,restrict["primary"],restrict["primary"])#如果有主键，为其创建索引
        cata[table]["index"][restrict["primary"]]=restrict["parmary"]
    if "unique" in restrict:
        for column in restrict["unique"]:
            cata[table]["unique"].append(column)

    catalog.updateCata(database,cata)
    return "表已经创建"

def dropTable(database,table):
    pass

def dropIndex(database,index):
    pass

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
    tablecontents=readTable(database,table,tableinfo["size"],tableinfo["format"])#这里暂时没有考虑buffer的问题
    check.checkRestrict(row,tablecontents,tableinfo)

    binaryrow=tobinary(row,tableinfo["format"])#转换成二进制
    insert(database,table,binaryrow,tableinfo["size"])
    tableinfo["length"]+=1
    catalog.updateCata(database,cata)
    return "插入了一行"
        


def deleteRow(database,table,condition):
    pass

def search(database,table,condition):
    pass
    

       