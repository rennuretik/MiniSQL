'''检查插入信息'''

import re

def checkRow(row,scheme):#检查一行是不是与scheme相匹配
    errormessage="数据格式错误"
    def match(x,y):#内部函数
        if y=="int":
            return isinstance(x, int)
        elif y=="float":
            return isinstance(x, float)
        else:
            if not isinstance(x, str):
                return False
            pat=re.compile(r"char\((\d+)\)")#正则表达式
            max=int(re.match(pat,y).group(1))#捕获所支持的字符串的最大长度
            return len(x.encode("utf8"))<=max#只支持utf8编码

    if len(row)!=len(scheme):
        raise Exception(errormessage)
    for x,y in zip(row,scheme):
        if not match(x,y):
            raise Exception(errormessage)

checkRow([1,"12364",3.5],["int","char(5)","float","float"])    
