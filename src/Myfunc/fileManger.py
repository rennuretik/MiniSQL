import os

def createFile(path):
    if os.path.isfile(path):
        raise Exception("the file is already exists")
    else:
        f=open(path,"w")
        f.close()

def createDir(path):
    if os.path.isdir(path):
        raise Exception("the directory is already exists")
    else:
        os.mkdir(path)

def insertRecord(file,record):
    pass

def deleteRecord(file,offset):
    pass