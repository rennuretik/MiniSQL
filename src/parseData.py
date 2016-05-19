'''
解析列表字典为字符串或者二进制数据
解析二进制数据为字符串或者字典或者列表
'''

import struct
import re

def parseScheme(scheme):#解析数据表的定义模式，返回供struct模块使用的模式和二进制格式的大小
    pattern=""
    charpat=re.compile(r"char\((\d+)\)")
    for item in scheme:
        if scheme[item]=="int":
            pattern+="i"
        elif scheme[item]=="float":
            pattern+="f"
        else:
            match=re.match(charpat,scheme[item])
            if match:
                pattern+=match.group(1)+"s"
            else:
                raise Exception("无法识别的类型")
    return pattern,struct.Struct(pattern).size#返回在文件当中存储的文件结构