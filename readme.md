#MiniSQL

基本功能实现

python minisql.py来运行程序

##运行说明

`\a` 显示当前所有的数据库

`\d` *database*· 切换数据库

`\t` 显示当前数据库

`help` 显示帮助

`\q` 退出数据库

###SQL 语句示例

支持的SQL语句不是很标准：

delete from r1 where  a>100 

create index index1 on tname  ( 3 )

create table aa (ii char(1),3 int, tet float, primary key ( 3 )) 

insert into db1 values (2,244,'fff','ttt')

select a,b from r1 where a>1.5 and a<2.3 sort by b desc

drop table 1111

import excel-name to table //从excel当中导入

***
代码写的惨不忍睹，bug多的数不胜数

功能几乎是糊出来的，和数据库几乎没有半毛钱关系

需要参考的也就凑合着参考一下吧

