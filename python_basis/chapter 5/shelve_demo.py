#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import shelve, pickle

class Student(object):
    def __init__(self, name):
        self.name = name

s = Student('steven')

she = shelve.open('shelve_test')
she['names'] = ['zhangsan', 'lisi', 'wangwu']  #持久化列表
she['student'] = s
she.close()

db = shelve.open('shelve_test')  #打开文件
names = db['names']
print(names)
student = db['student']
print(student.name)
db.close()  #关闭文件