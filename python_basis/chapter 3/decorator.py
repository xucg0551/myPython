#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import functools

#简单点的
def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(wrapper.__doc__)
        print('This is a logger decorator')
        func(*args, **kwargs)
    return wrapper


@logger  #等价于 test = logger(test)
def func1():
    print('this is func1')

@logger
def func2(p1, p2):
    '''
    :param p1:
    :param p2:
    :return:
    '''
    print('this is func2, and parameters is {} and {}'.format(p1, p2))

func1()
func2('zhangsan', 'lisi')

# #复杂点的  装饰器带有参数
# def decorator(type):
#     def logger(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             if type == 1:
#                 func(*kwargs, **kwargs)
#             else:
#                 print('type is wrong')
#         return wrapper
#     return logger
#
# @decorator(1)
# def func1(*args, **kwargs):
#     print('This is func1')

#
# @decorator(2)
# def func2(*args, **kwargs):
#     print('This is func2')

# func1()
# func2()
