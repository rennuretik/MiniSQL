import os,sys
import json

"""读取全局变量,"""
try:
    root=os.path.dirname(sys.path[0])
    f=open(os.path.join(root,"config.json"),"r")
    root=json.loads(f.read())["root"]#全局变量，程序的根目录
    f.close()
except:
    raise Exception("配置文件不存在")
    sys.exit()