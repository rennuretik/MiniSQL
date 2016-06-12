import re

def selectParser(SQL):
    lst = SQL.strip().split()

    if len(lst)==4 and lst[1] == "*" and lst[2]=="from":
        return ["select",lst[3],'*',None]

    if len(lst)==4 and lst[1] != "*" and lst[2]=="from":
        lst2 = lst[1].split(",")
        for i in range(0,len(lst2)):
            lst2[i] = lst2[i].strip()
            if lst2[i] == "": raise Exception("属性格式错误")
        lst1=["select",lst[3],lst2,None]
        return lst1

    if len(lst)==6 and lst[1] == "*" and lst[2]=="from" and lst[4] == "where":
        lst1 = SQL.split("where")[1].strip()
        lst1 = ["select", lst[3], "*", lst1]
        return lst1

    if len(lst)==6 and lst[1]!="*" and lst[2] == "from" and lst[4]== "where":
        lst1 = SQL.split("where")[1].strip()
        lst2 = lst[1].split(",")
        for i in range(0,len(lst2)):
            lst2[i] = lst2[i].strip()
            if lst2[i] == "": raise Exception("属性格式错误")
        lst1=["select",lst[3],lst2,lst1]
        return lst1
    else:
        raise Exception("句式错误")
