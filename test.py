'''import json

f=open("config.json","r")
data=f.read()
print(json.loads(data))'''

def p(a):
    def clojure(t):
        return t>a
    return clojure

c=p(5);
print(c(5))