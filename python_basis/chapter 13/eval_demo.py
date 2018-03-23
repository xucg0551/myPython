#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-


class Test():
    def fun(self):
        print('This is a eval test')


t = Test()
eval('t.fun()')