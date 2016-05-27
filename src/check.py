'''各种信息检查判断'''

import re
from fileManage import *

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
    for index,column in enumerate(tableinfo["scheme"]):
        if len(column)==2:
            continue
        elif column[2]=="unique" or column[2]=="primary":#这里暂时没有考虑索引
            for record in tablecontents:
                if row[index]==record[index]:
                    raise Exception("违反唯一性约束")
        else:
            raise Exception("表模式信息错误")

def  findindex(column,scheme):#找到一个table当中的一列所对于的index
    for index,x in enumerate(scheme):
        if column==x:
            return index
    raise Exception("没有找到这样的列")    

def parseCondition(condition):#解析筛选模式
    pat=re.compile(r"([a-z]+)(<>|<=|>=|<|>|=)(.*)")
    match=re.match(pat,condition)
    if not match:
        raise Exception("无法识别筛选信息")

    columnName=match.group(1)#列的名字
    operatorType=match.group(2)#是那种操作符号
    comparevalue=match.group(3)#进行比较的值
    return columnName,operatorType,comparevalue

def toClosure(condition,scheme):#把筛选字符串转换为一个判断的闭包
    if not condition:
        return lambda x: True
    columnName,operatorType,comparevalue=condition
    i=findindex(condition[0],scheme)
    def greathan(a,b):
        try:
            return a>type(a)(b)
        except:
            raise Exception("比较数据类型错误")

    def greateuqal(a,b):
        try:
            return a>=type(a)(b)
        except:
            raise Exception("比较数据类型错误")

    def lessthan(a,b):
        try:
            return a<type(a)(b)
        except:
            raise Exception("比较数据类型错误")

    def lessequal(a,b):
        try:
            return a<=type(a)(b)
        except:
            raise Exception("比较数据类型错误")    

    def equal(a,b):
        try:
            return a==type(a)(b)
        except:
            raise Exception("比较数据类型错误")

    def noName(row):
        if operatorType=="<":
            return lessthan(row[i],comparevalue)
        elif operatorType==">":
            return greathan(row[i],comparevalue)
        elif operatorType=="=":
            return equal(row[i],comparevalue)
        elif operatorType=="<>":
            return not equal(row[i],comparevalue)
        elif operatorType=="<=":
            return lessequal(row[i],comparevalue)
        elif operatorType==">=":
            return greatequal(row[i],comparevalue)

    return noName#返回判断函数的闭包

def toClosure2(database,contents,condition,tableinfo):
    if not condition:
        return lambda x: True
    if condition.find('and')!=-1:
        condition=condition.split("and")
        print(condition)
        if len(condition)>2:
            raise Exception("筛选条件过于复杂")
        for i in range(2):
            condition[i]=parseCondition(condition[i].strip()) 
        if not condition[0][0]==condition[1][0]:
            raise Exception("筛选条件过于复杂")
        '''if not ((condition[0][1]=="<" and condition[1][1]==">") or (condition[0][1]==">" and condition[1][1]=="<")) :
            raise Exception("不支持这样的筛选")#程序只支持在一个范围内的查找'''
        
        ind=findindex(condition[1][0],tableinfo["column"])
        func1=toClosure(condition[0],tableinfo["column"])
        func2=toClosure(condition[1],tableinfo["column"])#得到两个判断函数
        return [func1,func2]

    else:
        condition=parseCondition(condition)
        func=toClosure(condition,tableinfo["column"])
        return [func]

def fliterRow(database,contents,condition,tableinfo):#根据条件筛选出符合要求的记录
    if not condition:
        print(contents)
        for record in contents:
            yield record
        return
    if condition.find('and')!=-1:
        condition=condition.split("and")
        print(condition)
        if len(condition)>2:
            raise Exception("筛选条件过于复杂")
        for i in range(2):
            condition[i]=parseCondition(condition[i].strip()) 
        if not condition[0][0]==condition[1][0]:
            raise Exception("筛选条件过于复杂")
        '''if not ((condition[0][1]=="<" and condition[1][1]==">") or (condition[0][1]==">" and condition[1][1]=="<")) :
            raise Exception("不支持这样的筛选")#程序只支持在一个范围内的查找
        
        ind=findindex(condition[1][0],tableinfo["column"])
        if condition[0][1]=="<":
            hi=condition[0][2]
            lo=condition[1][2]
        else:
            hi=condition[1][2]
            lo=condition[0][2]#这个地方有点类型问题
        if hi<lo:
            return None#找到范围的上界和下界

        if str(ind) in tableinfo["inindex"]:#如果存在索引
            Btree=readIndex(database,tableinfo["inindex"][str(i)]) 
            pointers=Btree.finds(lo,hi)#从B树当中的找到范围
            for i in pointers:
                yield contents[i[1]]           
        else:'''
        func1=toClosure(condition[0],tableinfo["column"])
        func2=toClosure(condition[1],tableinfo["column"])#得到两个判断函数

        for row in contents:
            if func1(row) and func2(row):#如果两个条件都满足的话，返回这一行
                yield row

    else:
        condition=parseCondition(condition)
        func=toClosure(condition,tableinfo["column"])
        for row in contents:
            if func(row):
                yield row

if __name__=="__main__":
    con=parseCondition("a=5x")
    print(con)
    column=["a","b"]
    f=toClosure(con,column)
    print(f([6,"a"]))

#checkRow([1,"12364",3.5],["int","char(5)","float","float"])    
