import string
import re
import traceback
from create import *
from insert import *
from select import *
from drop import *
from delete import *

def process(SQL):
    SQL = SQL.strip().lower()
    SQL1 = SQL.split()
    lst = []
    if SQL1[0]=='create':
        lst = createParser(SQL)
    elif SQL1[0]=='select':
        lst = selectParser(SQL)
    elif SQL1[0]+SQL1[1]=='insert' + 'into':
        lst = insertParser(SQL)
    elif SQL1[0]=='drop':
        lst = dropParser(SQL)
    elif SQL1[0]=='delete':
        lst = deleteParser(SQL)
    elif SQL1[0] == '\d':
        lst = SQL1
        lst[0] = "changeDB"
    else:
        raise Exception("未知操作指令")
    return lst


if __name__ == "__main__":
    SQL = "delete * from r1 where a=b2131431 "
    SQL1 = "create index index1 on tname  ( 3 )"
    SQL2 = "create table aa (ii char(1),3 int, tet float, primary key ( 3 )) "
    SQL3 = "insert into db1 (2,244,'fff','ttt')"
    SQL4 = "select r1,r3 from r1 where a=b2131431 "
    SQL5 = "drop table 1111"
    print(process(SQL))
    print(process(SQL1))
    print(process(SQL2))
    print(process(SQL3))
    print(process(SQL4))
    print(process(SQL5))