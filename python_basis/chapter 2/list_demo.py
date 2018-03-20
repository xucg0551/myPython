#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import copy


names = ['xijinpin', 'likeqiang', 'lizhanshu', 'wangyang', 'wanghuning', 'zhaoleji', 'hanzhen', ['obama', 'bush']]
# print(names[0:-1])
# print(names[:])
# print(names[::2])
# print(names[::-1])
# print(names[-1:-4:-1])



# #浅拷贝和深拷贝
names_a = copy.copy(names)
names_b = copy.deepcopy(names)
names[-1].append('kliton')
names.append('jiangzeming')
print(names)
print(names_a)
print(names_b)
#
# print(names[-2:])
#
# #append() 列表末尾添加对象
# #count() 返回元素在列表中出现的次数
#
# #extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）。
# a_list = [123, 'xyz', 'zara', 'abc']
# b_list = [456, 'abc', '789']
# a_list.extend(b_list)
# print(a_list)
#
# #index() 函数用于从列表中找出某个值第一个匹配项的索引位置, 如果没有找到对象则抛出异常
# print(a_list.index('abc'))
#
# #insert() 函数用于将指定对象插入列表的指定位置
# a_list.insert(2, 'what')
# print(a_list)
#
# #pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
# print(a_list.pop(2))
# print(a_list)
#
# #remove() 函数用于移除列表中某个值的第一个匹配项
# c_list = ['xyz', 'zara', 'abc', 123, 'xyz']
# c_list.remove('abc')
# print(c_list)
#
# #reverse() 函数用于反向列表中元素
# d_list = [123, 'xyz', 'zara', 'abc', 'xyz'];
# d_list.reverse()
# print(d_list)

# def is_odd(n):
#     return n % 2 == 1
#
#
# newlist = filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# print(newlist)

# r = range(10, 100, 5)
# print(list(r))
#
# l = [1, 2, 3, 4, 5, 6]
# # print(type(l))
# # l = iter(l)
# # print(next(l))
# # print(type(l))
# #
# # # l = filter(lambda x: x % 2 == 0, l)
# # # print(list(l))
# # # print(list(l))
# sss = map(lambda x: x*2, filter(lambda x: x % 2 == 0, l))
#
# print(list(sss))

# s1 = 'hello world'
# s2 = copy.deepcopy(s1)
# s3 = copy.copy(s1)
#
# s1 = 'dsaffas'
#
# print(s1)
# print(s2)
# print(s3)
#
# l1 = [1, 3, 5, 7]
# l2 = copy.copy(l1)
# l3 = copy.deepcopy(l1)
#
# l1.append(9)
# print(l1)
# print(l2)
# print(l3)

d1 = {'k1':'v1', 'k2':'v2', 'k3':[1,2,3]}
d2 = copy.copy(d1)
d3 = copy.deepcopy(d1)

d1['k1'] = 'vvvv'
d1['k3'].append(4)

print(d1)
print(d2)
print(d3)

