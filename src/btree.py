class Btree(object):
    """docstring for Btree"""

    class Node(object):#内部类，B+树的子节点
        """docstring for Node"""
        def __init__(self,isLeaf,hi,parent=None):
            self.values=[None for x in range(hi)]
            self.pointers=[None for x in range(hi+1)]
            self.size=0
            self.isLeaf=isLeaf
            self.parent=None
            self.hi=hi

        def insert(self,key,offset):
            if key in self.values:
                return 

            if self.size==0:
                self.values[0]=key
                self.pointers[0]=offset   
                self.size+=1
                return 
            
            for i in range(0,self.size):
                if key<self.values[i]:
                    self.values.insert(i,key)
                    self.pointers.insert(i,offset)
                    self.values.pop() #插入到合适的地方并删除多余的元素
                    if self.isLeaf:
                        del self.pointers[self.hi-1]
                    else:
                        del self.pointers[self.hi]
                    self.size+=1
                    return

            self.values[self.size]=key
            self.pointers[self.size+1]=self.pointers[self.size]
            self.pointers[self.size]=offset
            self.size+=1

        def clear(self):
            for i in  range(0,self.hi):
                self.values[i]=None
                self.pointers[i]=None
            self.size=0

        def clearall():
            self.values=[None for x in range(hi)]
            self.pointers=[None for x in range(hi+1)]
            self.size=0
                       
    def __init__(self, records=[],where=0,lo=2,hi=3):#records是记录的集合，生成一个指针的B树
        self.root=self.Node(True,hi)
        self.height=0
        self.where=where
        self.lo=lo
        self.hi=hi
        for offset,a in enumerate(records, start=0):
            insert(a[where],offset)

    def copyvalue(self,From,to,end,start=0):
        for i in range(start,end):
            to.values[i-start]=From.values[i]

    def copypointer(self,From,to,end,start=0):
        for i in range(start,end):
            to.pointers[i-start]=From.pointers[i]                        

    def insert(self,key,offset):#插入一条记录
        node=self.findLeaf(key)
        if node.size<self.hi:
            node.insert(key,offset)
        else:
            temp=self.Node(False,self.hi+1)
            self.copyvalue(node,temp,self.hi)
            self.copypointer(node,temp,self.hi)
            temp.size=self.hi
            #print(temp.values)
            #print(temp.pointers)
            temp.insert(key,offset)#复制
            #print(temp.values)
            #print(temp.pointers)


            new=self.Node(True,self.hi)
            new.pointers[self.hi]=node.pointers[self.hi]
            node.pointers[self.hi]=new#改变指针

            node.clear()
            self.copyvalue(temp,node,(self.hi+1)//2)
            self.copypointer(temp,node,(self.hi+1)//2)
            node.size=(self.hi+1)//2
            self.copyvalue(temp,new,self.hi+1,(self.hi+1)//2)
            self.copypointer(temp,new,self.hi+1,(self.hi+1)//2)
            new.size=self.hi+1-(self.hi+1)//2
            self.insertParent(node,new.values[0],new)


    def insertParent(self,left,key,right):
        if left==self.root:
            newroot=self.Node(False,self.hi)
            newroot.values[0]=key
            newroot.pointers[0]=left
            newroot.pointers[1]=right
            self.root=newroot
            left.parent=newroot
            right.parent=newroot#生长出新的根节点,更新left和right的父亲节点
        else:
            parent=left.parent
            if parent.size<self.hi:
                parent.insert(key,right)
                right.parent=parent#如果有空位直接插入即可
            else:
                temp=self.Node(False,self.hi+1)
                self.copyvalue(parent,temp,self.hi)
                self.copypointer(parent,temp,self.hi)
                temp.insert(key,right)#复制

                new=self.Node(False,self.hi,parent.parent)
                parent.clearall()
                self.copyvalue(temp,parent,(self.hi+1)//2)
                self.copypointer(temp,parent,(self.hi+1)//2+1)
                parent.size=(self.hi+1)//2;
                self.copyvalue(temp,new,self.hi+1,(self.hi+1)//2)
                self.copypointer(temp,new,self.hi+2,(self.hi+1)//2+1)
                new.size=self.hi+1-(self.hi+1)//2
                insertParent(P,temp.values[(self.hi+1)//2],new)

    def findLeaf(self,key):#找到某个记录应该在的子节点
        current=self.root
        while not current.isLeaf:
            for i in range(0,current.size):
                if key<current.values[i]:
                    current=current.pointers[i]
                    break
                current=current[current.pointer[current[size]]]#到最右边的节点
        return current

    def printtree(self,current):
        if not current.isLeaf:
            print(current.values)
            for x in current.pointers:
                if x:
                    self.printtree(x)
        else:
            print(current.values, end=' ')
            print(current.pointers,end=' ')
            if current.pointers[self.hi]:
                self.printtree(current.pointers[self.hi])            

B=Btree()    
B.insert("x",35)
B.insert("s",18)
B.insert("y",135)
B.insert("q",2)
B.insert("a",54)
B.printtree(B.root)
        





