#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

# class Student(object):
#     pass
#
#
# def play(what):
#     print('play {}'.format(what))
#
#
# s1 = Student()
# s2 = Student()
# s3 = Student()
# s1.name = 'Steven'  #给实例s1绑定属性
# s2.play = play  #给实例s2绑定属性
#
#
# #hasattr getattr setattr
# if hasattr(s1, 'name'):
#     print(getattr(s1, 'name'))
#
# if hasattr(s2, 'play'):
#     p_func = getattr(s2, 'play')
#     p_func('football')
#
# if not hasattr(s3, 'play'):
#     setattr(s3, 'play', play)
#     p_func = getattr(s3, 'play')
#     p_func('basketball')

# #private变量
# class Student(object):
#     def __init__(self, name, age):
#         self.__name = name   #_name变量外部也是可以访问的，但当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”
#         self.__age = age    #变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，特殊变量是可以直接访问的，不是private变量，
#
# s1 = Student('steven', 18)
# s1.__age = 20  #这种动态添加属性，注意的是:__age变量和class内部的__age变量不是一个变量，内部的__age已经被python解释器自动改成了_Student__age
# # print(s1.__age)
# print(s1._Student__age)  #访问private变量


#__str__
# class Student(object):
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return 'Student object (name: {})'.format(self.name)
#
#     __repr__ = __str__
#
# print(Student('steven'))

# #__getattr__
# class Chain(object):
#     def __init__(self, path=''):
#         self.path = path
#
#     def __getattr__(self, item):
#         return Chain('{}/{}'.format(self.path, item))
#
#     def __str__(self):
#         return self.path
#
#     __repr__ = __str__
#
# path = Chain().status.user.timeline.list
# print(path)

# _*_coding:utf-8_*_


# class A:
#     def __init__(self):
#         self.n = 'A'
#
#
# class B(A):
#     # def __init__(self):
#     #     self.n = 'B'
#     pass
#
#
# class C(A):
#     def __init__(self):
#         self.n = 'C'
#
#
# class D(B, C):
#     # def __init__(self):
#     #     self.n = 'D'
#     pass
#
#
# obj = D()
#
# print(obj.n)

# #staticmethod  classmethod
# class Dog(object):
#     '''
#     fsdafsafadsfdsaf
#     '''
#     _game = 'basketball'
#     def __init__(self,name):
#         self.name = name
#         self.dict = {}
#
#     def __call__(self, *args, **kwargs):
#         print('call...')
#
#     def __setitem__(self, key, value):
#         self.dict[key] = value
#
#     def __getitem__(self, item):
#         return self.dict[item]
#
#     def __delitem__(self, key):
#         print('__delitem__')
#
#     @staticmethod
#     def eat():
#         print(" is eating")
#
#     @classmethod
#     def play(cls):
#         print('play {}'.format(cls._game))
#
#     @property
#     def age(self):
#         return self._age
#
#     @age.setter
#     def age(self, value):
#         self._age = value
#
#     @age.deleter
#     def age(self):
#         print('delete...')
#
#
#
# # Dog.play()
# d = Dog("ChenRonghua")
# # d.play()
# # # Dog.eat()
# # d.age = 10
# # print(d.age)
# # del d.age
# # print(d.__module__)
# # print(d.__class__)
# # print(Dog.__name__)
# # print(d.__doc__)
# # d()
# d['name'] = 'a_cai'
# del d['name']
# print(d['name'])

# def func(self):
#     print('hello {}'.format(self.name))
#
# def __init__(self, name, age):
#     self.name = name
#     self.age = age
#
# Foo = type('Foo', (object, ), {'func':func, '__init__':__init__})
# f = Foo('jack', 22)
# f.func()

class MyType(type):
    def __init__(self, *args, **kwargs):
        print('MyType __init__', *args, **kwargs)

    def __call__(self, *args, **kwargs):
        print('MyType __call__', *args, **kwargs)
        obj = self.__new__(self)
        print('obj ', obj, *args, **kwargs)
        print(self)
        self.__init__(obj, *args, **kwargs)
        return obj

    def __new__(cls, *args, **kwargs):
        print('MyType __new__', *args, **kwargs)
        return type.__new__(cls, *args, **kwargs)

class Foo(object, metaclass=MyType):
    def __init__(self, name):
        self.name = name
        print('Foo __init__')

    def __new__(cls, *args, **kwargs):
        print('Foo __new__', *args, **kwargs)
        return object.__new__(cls)

f = Foo('steven')
