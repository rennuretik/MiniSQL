import json
import os
import sys
import api
import catalog
from fileManage import *

#print(api.deleteRow("test","test","b>5 and b<=6.7"))

b = readTable("test", "test", 18, "<10sd")
print(list(b))
btree = readIndex("test", "test0")
btree.pretty()


#api.dropIndex("test","test","test")
#api.dropTable("test","test")

#tree=readIndex("test","test")
#tree.pretty()

#api.insertRow("test","test1",["f",3])

#api.createIndex("test","test","b","test0")

#api.createTable("test","test",[["a","char(10)","unique"],["b","float","unique"]],{"unique": ["a","b"]})
#api.createTable("test","test1",[["a","char(10)","unique"],["b","int","unique"]],{"unique": ["a","b"]})

'''api.insertRow("test","test",["a",4.5])
api.insertRow("test","test",["b",5.5])
api.insertRow("test","test",["c",6.5])
api.insertRow("test","test",["d",6.6])
api.insertRow("test","test",["e",6.7])
api.insertRow("test","test",["f",6.8])
api.insertRow("test","test",["abh",3.6])'''

'''b=readTable("test","test",14,"<10sf")
print(list(b))'''

#api.createDatabase("test")

#api.createDatabase("test")

'''f=open("config.json","r+")
js=f.read()
js=json.loads(js)
js['default']="truth"
js=json.dumps(js,indent=4)
print(js)'''




