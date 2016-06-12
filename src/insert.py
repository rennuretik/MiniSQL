import re

def insertParser(SQL):
    lst = SQL.split()#check the second word
    if len(lst) < 4: raise Exception("部分信息缺失")#因为括号中可能有空格的原因不能定长，但至少要有5个元素
    if re.search("\(\s*[a-z,'0-9]+\s*\)",SQL)==None: raise Exception("插入数据格式错误")#判断能否找到()
    elif (SQL[-1]!=')'): raise Exception("括号错误")#确定最后一位一定是')'

    str = (SQL.split("(",1)[1].strip())[:-1]
    lst1 = str.split(",")
    str = ""
    for i in range(0,len(lst1)):
        lst1[i] = lst1[i].strip()
        if lst1[i] == "": raise Exception("插入数据格式错误")
        str += lst1[i] +","
    # if len(lst1)!=str.count(",") + 1:raise Exception("插入数据格式错误")
    str = str[:-1]
    str = "["+ str+"]"
    lst1 = eval(str)
    lst = ["insert", lst[2], lst1]
    return lst