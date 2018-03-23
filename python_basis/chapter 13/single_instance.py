#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

# import threading
# class Singleton(object):
#     _instance_lock = threading.Lock()
#
#     def __init__(self):
#         pass
#
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Singleton, "_instance"):
#             with cls._instance_lock:
#                 if not hasattr(cls, "_instance"):
#                     cls._instance = object.__new__(cls)
#         return cls._instance
#
# obj1 = Singleton()
# obj2 = Singleton()
# print(obj1,obj2)
#
# def task(arg):
#     obj = Singleton()
#     print(obj)
#
# for i in range(10):
#     t = threading.Thread(target=task,args=[i,])
#     t.start()

#装饰器实现
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class A(object):
    a = 1

    def __init__(self, x=0):
        self.x = x


a1 = A(2)
a2 = A(3)
print(a1,a2)