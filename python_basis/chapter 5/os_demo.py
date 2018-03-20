#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import os

# 查看当前目录的绝对路径 abspath
print(os.path.abspath('.'))

#添加新的路径 join
print(os.path.join(os.path.abspath('.'), 'testdir'))

#将path分割成目录和文件名二元组返回
print(os.path.split(__file__))
print(os.path.splitext(__file__))  #可以用来判断文件的后缀

#返回path的目录
print(__file__)
print(os.path.dirname(__file__))
print(os.path.basename(__file__))  #返回path最后的文件名。如何path以／或\结尾，那么就会返回空值。即os.path.split(path)的第二个元素

#如果path存在，返回True；如果path不存在，返回False
print(os.path.exists(__file__))

#如果path是绝对路径，返回True
print(os.path.isabs(__file__))

#如果path是一个存在的文件，返回True。否则返回False
print(os.path.isfile(__file__))

#如果path是一个存在的目录，则返回True。否则返回False
print(os.path.isdir(__file__))

#列出指定目录下的所有文件和子目录，包括隐藏文件，并以列表方式打印
print(os.listdir('.'))

#获取当前工作目录，即当前python脚本工作的目录路径
print(os.getcwd())

print(os.name) #win->'nt'; Linux->'posix'
print(os.uname())
print(os.environ)
print(os.stat(__file__))
print(os.sep)
print(os.pathsep)
os.system("bash command")