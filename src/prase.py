'''
    解析SQL语句的模块
'''

def prase(SQL):
    return command

'''
    输入一条简单的SQL语句，参见实验指导书
    输出是一个列表，包括操作的类型，操作的表，操作的值，约束

    例如：
    SQL: "create database test"
    command: ["create database","test"]

    SQL: "create table test"
    command: ["create table","test"]
    
    SQL: "create table (a int, b char(5),primary key a)"
    command: ["create table",{"a":"int","b": "char(5)" },{"a":"primary","b":None}]
    #第二项是一个字典，包含了属性名和它的类型
    #第三项也是一个字典，包含属性和它的约束
    
    drop index、drop table、drop database与create database，create table相似
    
    SQL: create index index on table(key)
    command: ["create index ","index","table","key"]
    
    SQL: select row1,row2 from student where row 1>5;
    command: ["select","student",[row1,row2]，"row1>5"]
    
    SQL: insert into table values(a,b)
    command:["insert","table",[a,b]]
   
    delete 与select类似

    各种查询约束条件先返回字符串（或者是字符串的列表）即可
    尽管我只写了一个函数，但不要在一个函数里写完所有与事情，在几个文件里写完也是可以的
    不要完全用if-elif来写，推荐使用正则表达式（标准库里re模块）
    如果做完了比较闲可以考虑把约束条件换成闭包（就是一个函数），闭包示例：
    def p(a):
        def closure(row1):
            return t>a
    return clojure

    c=p(5);
    c(4)=>False
    c(6)=>True
    比如约束条件"row1>5"应该换成一个上面c那样的函数，觉得困难就返回一个字符串也行
'''