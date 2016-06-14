from process import *
from globalvs import *
from api import *


def helpuser():  # help information
    print("support simple SQL language")
    print("'\d database' to change database")
    print("'\\a' to show all the database")
    print("'\\t' to show all the tables in the current database")


def about():  # print about information in the beginning
    print("MiniSQL version 1.1, thanks for trying")
    print("input help for help, \q to quit")


def showdbs():  # show all the databases
    print("all the databases:")
    for db in DBs:
        print(db)


def showtables():  # show all the table in the current database
    print("all the tables")
    tables = findalltable(currentDB)
    for x in tables:
        print(x)


def changedb(database):  # change database
    global currentDB;
    if database in DBs:
        currentDB = database
    else:
        raise Exception("数据库不存在")
    return "database changed"

'''
def foo0(args):  # changeDB
    changedb(args[1])
    return "database changed"


def foo1(args):
    createDatabase(args[1])
    return "database created"


def foo2(args):
    deleteDatabase(args[1])
    return "database dropped"

def foo4(args):
    dropTable(currentDB,args[1])
    return "table dropped"


def foo5(args):
    createIndex(currentDB,args[2],args[3],args[1])
    #api.createIndex("test","test","b","test0")
    #['create index', 'index1', 'tname', '3']
    return "index created"


def foo6(args):
    dropIndex(currentDB,args[2],args[1])
    return "index dropped"


def foo7(args):
    insertRow(currentDB,args[1],args[2])
    return "1 row inserted"
    #['insert', 'a', [2, 244, 'fff', 'ttt']]

def foo8(args):
    return deleteRow(currentDB,args[1],args[2])


def foo9(args):
    return search(currentDB,args[1],args[2],args[3])'''

def createtable(args):
    scheme=[]
    for x in args[2]:
        if x in args[4]:
            scheme.append([x, args[2][x], "unique"])
        else:
            scheme.append([x, args[2][x], args[3][x]])
    restrict={
        "unique" : [],
        "primary" : None
    } 
    for y in args[3]:
        if args[3][y]=="unique":
            restrict["unique"].append(y);
        elif args[3][y]=="primary key":
            restrict["primary"]=y;
    return createTable(currentDB,args[1],scheme,restrict)
    
    #['create table', 'xxx', {'a': 'int', 'b': 'char(5)'}, {'a': 'primary key', 'b': 'None'}, ['b']]
    #api.createTable("test","test",[["a","char(10)","unique"],["b","float","unique"]],{"unique": ["a","b"]})

functions = {
    "changeDB": lambda args: changedb(args[1]),
    "create database": lambda args: createDatabase(args[1]),
    "drop database": lambda args: deleteDatabase(args[1]),
    "create table": lambda args: createtable(args),
    "drop table": lambda args: dropTable(currentDB,args[1]),
    "create index": lambda args: createIndex(currentDB,args[2],args[3],args[1]),
    "drop index":  lambda args: dropIndex(currentDB,args[2],args[1]),
    "insert": lambda args: insertRow(currentDB,args[1],args[2]),
    "delete": lambda args: deleteRow(currentDB,args[1],args[2]),
    "select": lambda args: search(currentDB,args[2], args[1],args[3],args[4],args[5]),
    "import": lambda args: importExcel(currentDB,args[1],args[2])
}


if __name__ == "__main__":
    about()
    command = ""
    while command != "\q":
        print(currentDB+">>>", end="")
        command = input().lower()
        if command == "\q":
            print("goodbye")
            exit()
        elif command == "help":
            helpuser()
        elif command == "\\a":
            showdbs()
        elif command == "\\t":
            showtables()
        else:
            operation = process(command)
            print(operation)
            backInfo = functions[operation[0]](operation)
            print(backInfo)
            '''except Exception as e:print(e)'''



