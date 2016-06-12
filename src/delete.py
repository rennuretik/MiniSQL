import re

def deleteParser(SQL):
    lst = SQL.strip().split()
    lst1 = SQL.split("where")[1].strip()
    if (lst[1] == "from" and lst[3] == "where"):
        lst1=["delete",lst[2],lst1]
        return lst1
    else:
        raise Exception("句式错误")
