'''
解析列表字典为字符串或者二进制数据
解析二进制数据为字符串或者字典或者列表
'''

import struct
import re

def parseScheme(scheme):#解析数据表的定义模式，返回供struct模块使用的模式和二进制格式的大小
    pattern="<"
    charpat=re.compile(r"char\((\d+)\)")#解析char类型的正则表达式
    for item in scheme:
        if item[1]=="int":
            pattern+="i"
        elif item[1]=="float":
            pattern+="d"
        else:
            match=re.match(charpat,item[1])
            if match:
                pattern+=match.group(1)+"s"
            else:
                raise Exception("无法识别的类型")
    return pattern,struct.Struct(pattern).size#返回在文件当中存储的文件结构

def tobinary(row,pat):#把一行的信息转换成二进制

    def topats(pat):#内部函数，把pat转换成pats列表
        a="<"
        for x in pat:
            if x=="<":
                continue
            elif x.isdigit():
                a+=x
            else:
                yield a+x
                a="<"
        return pats

    binarydata=b""
    pats=topats(pat)
    for p,d in zip(pats,row):
        binarydata+=struct.pack(p,d.encode("utf8") if isinstance(d, str) else d)
    return binarydata

def toRecord(row,pat):#把二进制数据转换成人类可阅读的列表
    a=list(struct.unpack(pat,row))
    for index,x in enumerate(a):
        if isinstance(x, bytes):
            a[index]=x.decode("utf8").strip("\x00")#去除掉多余的空字符
    return a

'''pat="<10si"
text=["夏爽",351]
binary=tobinary(text,pat)
print(toRecord(binary,pat)[0])

b=tobinary(["夏爽",35,2.5],"<10sif")
print(len(b))
c=struct.unpack("<10sif",b)
print(c)'''

