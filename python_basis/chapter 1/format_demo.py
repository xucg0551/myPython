#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

#http://www.runoob.com/python/att-string-format.html

import sys

print(sys.path)

# 1.位置
print('I am {}, age {}'.format('steven', 18))
print('I am {0}, age {1}, really {0}'.format('steven', 18))


#2.list
print('I am {0}, age {1}, really {0}'.format(*['steven', 18]))
print('I am {}, age {}'.format(*['steven', 18]))

#2.. 单个列表
print('I am {0[0]}, age {0[1]}, really {0[0]}'.format(['steven', 18]))

#2.. 多个列表
print('I am {0[0]}, age {0[1]}; He is {1[0]}, age {1[1]}'.format(['alen', 20], ['steven', 18]))

#3.dict --->参数直观
person_dict = {'name': 'steven', 'age': 18, 'province':'jiangsu'}
print('I am {name}, age {age}, province {province}'.format(**person_dict))

#4.关键字
print('I am {name}, age {age}'.format(name='steven', age=18))

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person('steven', 18)
print('I am {p.name}, age {p.age}'.format(p=p))

#填充与对齐  ^, <, > 分别是居中、左对齐、右对齐，后面带宽度  :号后面带填充的字符，只能是一个字符
print('{:x>10}'.format(123456))
print('{:x<10}'.format(123456))
print('{:x^10}'.format(123456))

#精度与类型
print('{:.2f}'.format(321.456789))

#用来做金额的千位分隔符
print('{:,}'.format(1234567890))

#b、d、o、x分别是二进制、十进制、八进制、十六进制
print('{:b}, {:o}, {:d}, {:x}'.format(15, 15, 15, 15))
