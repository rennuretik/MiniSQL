import os,sys
import json

"""读取全局变量,"""
DBs = []

try:
    root = os.path.dirname(sys.path[0])
    f = open(os.path.join(root, "config.json"), "r")
except Exception as e:
    raise Exception("配置文件不存在")

configInfo = json.loads(f.read())
root = configInfo["root"]  # 全局变量，程序的根目录

for x in configInfo["databases"]:
    if configInfo["databases"][x]:
        DBs.append(x)  # 现有的所有数据库

defaultDB = configInfo["default"]
currentDB = configInfo["default"]


def updateconfig():  # 更新数据库信息
    configInfo = json.loads(f.read())

    for x in configInfo["databases"]:
        if configInfo["databases"][x]:
            DBs.append(x)  # 现有的所有数据库'




