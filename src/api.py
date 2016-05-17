import catalog
import tableFile
import fileManage

def createDatabase(name):
    config=catalog.readConfig()
    if name in config["databases"]:
        raise Exception("数据库已经存在")
    else:
        fileManage.initialDB(name)#初始化文件
        config["databases"][name]=True
        catalog.updateConfig(config)#更新全局配置

def deleteDatabase(name):
    config=catalog.readConfig()
    if name not in config["databases"]:
        raise Exception("数据库不存在")
    else:
        fileManage.deleteDB(name)
        del config["databases"][name]
        catalog.updateConfig(config)

def createTable(database,table,scheme,restrict={}):
    catalog=catalog.readCata()
    if table in catalog:
        raise Exception(table+"表已经存在")
    catalog[table]=scheme
    catalog[table+"restrict"]=restrict
    catalog[table+"_length"]=0
    catalog[table+"_index"]={}
    fileManage.newTable(database,table,scheme)
    if restrict["parmary"]:
        createIndex(database,table,restrict["primary"],restrict["primary"])#如果有主键，为其创建索引
        catalog[table+"_index"][restrict["primary"]]=restrict["parmary"]
    catalog.updateCata(database,catalog)
    return "表已经创建"



def createIndex(database,table,index,column):
    pass

def dropTable(database,table):
    pass

def dropIndex(database,index):
    pass

def insertRow(database,table,row):
    pass

def deleteRow(database,table,condition):
    pass

def search(database,table,condition):
    pass
    

       