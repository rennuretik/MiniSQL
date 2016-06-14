import re
import collections


def createParser(SQL):
    lst = SQL.split()  # check the second word
    # create database xxx
    if (lst[1]=="database") :
        if(len(lst)==3):  # 符合格式
            lst = [lst[0]+" "+lst[1],lst[2]]
            return lst
        else:raise Exception("数据库命名错误")

    # create table xxx (a, int, b char(5), primary key ( a ))
    if (lst[1] == "table") :
        if len(lst)<=3: 
            raise Exception("表名信息缺少")
        pattern_type = {"int","float"}
        dic_constraint = {}
        unique_constraint=[]
        dic_col_name = collections.OrderedDict()
        k = "~" #初始化k，用于记录primary key出现的位置

        if (re.match("\(" , lst[3])==None) or (SQL[-1]!=")"): raise Exception("括号错误")#这个句法必须要有括号
        str = (SQL.split("(",1)[1]).strip()#获取 "create table"之后括号中的内容 "(.......)"

        str = str[:-1]#去掉最后的")"
        lst1 = str.split(",")#获得括号中的属性以及类型，成组，如"a int"," b char(5)"," primary key (a)"
        for i in range(0,len(lst1)):#对每个lst中的str操作：
            lst1[i] = lst1[i].strip()#去除空格'a int', 'b char(5)', 'primary key (a)'
            if re.match("primary key \(\s*[a-z0-9]+\s*\)",lst1[i]):#寻找primary key出现的位置
                dic_constraint = { (lst1[i].split("(")[1].split(")")[0]).strip() : "primary key" }#记录在constraint字典中
                # dic_constraint = eval(dic_constraint)
                k = i
                continue
        if (k!="~"):lst1.remove(lst1[k])#将primary key (xxx)移除，剩下是都是属性定义部分，若没有定义，k="~"，不执行该句
        for i in range(0,len(lst1)):#剩下的属性定义部分，应符合字典的套路一一对应
            if len(lst1[i].split())!=2:
                if (len(lst1[i].split())==3 and lst1[i].split()[2]!='unique'): raise Exception("表属性定义格式错误")#除了二个词组成的和三个词且最后是unique的都记错误
                else:unique_constraint.append(lst1[i].split()[0])

            lst2 = lst1[i].split()#拆分
            # for j in range(0,2):
            #     lst2[j] = "\""+lst2[j]+"\""

            if (lst2[1] not in pattern_type) and (re.match("char\([0-9]+\)",lst2[1]))==None: raise Exception("属性的类型定义格式错误")#判断是否为int float char(324234)这三种情况
            dic_col_name[lst2[0]] = lst2[1]#记录到column字典中
            if (lst2[0] not in dic_constraint) : dic_constraint[lst2[0]] = "None"#补全非主键的信息
        for item in dic_constraint:
            if item not in dic_col_name:raise Exception("主键不是属性名")#若主键名不存在column中，报错
        lst = ["create table", lst[2],dic_col_name,dic_constraint,unique_constraint]
        return lst

    # create index xxx
    if (lst[1]=="index") :
        if len(lst)< 6: raise Exception("部分信息缺失")#因为括号中可能有空格的原因不能定长，但至少要有5个元素
        elif lst[3]!="on" : raise Exception("'on'语法错误")#判断on的是否在第4个位置

        if re.search("\(\s*[a-z0-9]+\s*\)",SQL)==None: raise Exception("找不到建立index的属性")#判断能否找到()
        elif (SQL[-1]!=")"): raise Exception("括号错误")#确定最后一位一定是')'

        str = (SQL.split("(",1)[1])
        str = str[:-1].strip()
        lst = ["create index", lst[2], lst[4], str]
        return lst

    else: raise Exception("未知"+lst[1]+"指令")

if __name__=="__main__":
    print(createParser('create table xxx (a int, b char(5) unique, primary key ( a ))'))
