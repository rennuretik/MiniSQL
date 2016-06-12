import re

def dropParser(SQL):
    lst = SQL.split()#check the second word
    if lst[1]=="index":
        if(len(lst)==5):#符合格式
            lst = [lst[0]+" "+lst[1],lst[2],lst[4]]
            return lst
        else:raise Exception("索引名错误")
    elif lst[1]=="database":
        if(len(lst)==3):#符合格式
            lst = [lst[0]+" "+lst[1],lst[2]]
            return lst
        else:raise Exception("数据库名错误")
    elif lst[1]=="table":
        if(len(lst)==3):#符合格式
            lst = [lst[0]+" "+lst[1],lst[2]]
            return lst
        else:raise Exception("表名错误")
    else:raise Exception("未知"+lst[1]+"指令")