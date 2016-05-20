'''检查插入信息'''

import re

def checkFormat(row,scheme):#检查一行是不是与scheme相匹配
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

def checkRestrict(row,tablecontents,tableinfo):
    if "unique" not in tableinfo:
        return
    for index,column in enumerate(tableinfo["scheme"].values()):
        if len(column)==2:
            continue
        elif column[2]=="unique" or column[1]=="primary":#这里暂时没有考虑索引
            for record in tablecontents:
                if row[index]==record[index]:
                    raise Exception("违反唯一性约束")
        else:
            raise Exception("表模式信息错误")



#checkRow([1,"12364",3.5],["int","char(5)","float","float"])    
