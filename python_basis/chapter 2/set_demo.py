#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(type(a))

print(a.symmetric_difference(b))
print(a.difference(b))
print(a.union(b))
print(a.issubset(b))
