import json
import os
import sys
import api
import catalog
from fileManage import *

api.createTable("test","test",{"a": "char(5)","b": "int"},{"unique":["a","b"]})
#api.createDatabase("test")

#api.createDatabase("test")

'''f=open("config.json","r+")
js=f.read()
js=json.loads(js)
js['default']="truth"
js=json.dumps(js,indent=4)
print(js)'''




