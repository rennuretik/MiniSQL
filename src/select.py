def selectParser(SQL):
    lst=SQL.split()
    if lst[2]!="from":
        raise Exception("SQL语句错误")
    if "where" not in lst:
        if "sort" not in lst:
            if len(lst)!=4:
                raise Exception("SQL语句错误")
            return [lst[0], lst[1].split(','), lst[3], None, None, False]
        j=lst.index("sort")
        if len(lst)<j+3 or lst[j+1]!= "by":
            raise Exception("SQL语句错误")
        if lst[-1] != "desc":
            return [lst[0], lst[1].split(','), lst[3], None, lst[j+2] , False]
        return [lst[0], lst[1].split(','), lst[3], None, lst[j+2] , True]
    if lst.index("where")!=4:
        raise Exception("SQL语句错误")
    if "sort" not in lst:
        return [lst[0], lst[1].split(','), lst[3], ' '.join(lst[5:]), None, False]
    i=lst.index("sort")
    if len(lst)<i+3 or lst[i+1]!= "by":
        raise Exception("SQL语句错误")
    if lst[-1] != "desc":
        return [lst[0], lst[1].split(','), lst[3], ' '.join(lst[5:i]),lst[i+2] , False]
    return [lst[0], lst[1].split(','), lst[3], ' '.join(lst[5:i]),lst[i+2] , True]

if __name__=="__main__":
    print(selectParser('select * from test'))
    print(selectParser('select a,b from test where a>5 and b<7'))
    print(selectParser('select a,b from test where a>5 and b<7 sort by a'))
    print(selectParser('select a,b from test where a<4 sort by b desc'))

    '''select * from test'''
    '''select a,b from test where a>5 and b<7'''
    '''select a,b from test where a>5 and b<7 sort by a'''
    '''select a,b from test where a<4 sort by b desc'''  #




