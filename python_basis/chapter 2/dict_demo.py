#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

#clear() 清空内容
a_dict = {'name': 'steven', 'age': 18}  #或者 a_dict = dict(name='steven', age=18)
print(a_dict)
a_dict.clear()
print(a_dict)

#fromkeys() 函数用于创建一个新字典，以序列seq中元素做字典的键，value为字典所有键对应的初始值。
keys = ['name', 'age', 'sex']
a_dict = dict.fromkeys(keys)
print(a_dict)
a_dict = dict.fromkeys(keys, 10)
# vals = ['steven', '20', 'male']
# a_dict = dict.fromkeys(keys,vals)
print(a_dict)

#update() 函数把字典dict2的键/值对更新到dict里，该函数没有返回值  用法 dict1.update(dict2)
dict_a = {'name':'steven', 'age': 10}
dict_b = {'name':'alen'}

dict_a.update(dict_b)
print(dict_a)

#keys() 函数以列表的形式返回字典的所有键
dict_c = {'name':'steven', 'age': 10}
print(dict_c.keys())

#values() 函数以列表的形式返回字典的所有值
print(dict_c.values())

#pop() 方法删除字典给定键 key 所对应的值，返回值为被删除的值
print(dict_c.pop('age'))
if 'age' not in dict_c:
    print('false')

#setdefault() 如果键不存在于字典中，将会添加键并将值设为默认值，若存在，则返回该键对应的值
dict_d = {'name':'steven'}
print(dict_d.setdefault('age', 18))
print(dict_d.keys())

#popitem() 方法随机返回并删除字典中的一对键和值
dict_e = {'name':'steven', 'age':19, 'sex':'male', 'score':85}
print(dict_e.popitem())
