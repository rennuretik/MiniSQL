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

for x in configInfo["databases"]:
    if configInfo["databases"][x]:
        DBs.append(x)  # 现有的所有数据库

defaultDB = configInfo["default"]
currentDB = configInfo["default"]








