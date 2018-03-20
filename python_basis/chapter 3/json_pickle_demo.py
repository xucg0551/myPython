#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import pickle, json
data = {'k1': 123, 'k2': 'Hello'}


#pickle
#pickle.dumps 将数据通过特殊的形式为只有python语言认识的字符串
pickle_str = pickle.dumps(data)
print('pickle_dumps_type:', type(pickle_str))
print('pickle_loads:', pickle.loads(pickle_str))

with open('result.pk', 'wb') as fp:
    pickle.dump(data, fp)

with open('result.pk', 'rb') as fp:
    pickle_str_ = pickle.load(fp)
    print('pickle_load:', pickle_str_)


#json 可以序列化的类型dict, list, str, int, float, true, false
#json.dumps 将数据通过特殊形式转换为所有程序语言都认识的字符串
json_str = json.dumps(data)
print('json_dumps_type:', type(json_str))
print('json_loads:', json.loads(json_str))

with open('result.json', 'w') as fp:
    json.dump(data, fp)

with open('result.json', 'r') as fp:
    json_str_ = json.load(fp)
    print('json_load:', json_str_)

#如果要序列化一个类的对象？ 对象的__dict__
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('张三', 20, 88)

#ensure_ascii 针对中文
print(json.dumps(s, ensure_ascii=False, default=lambda obj: obj.__dict__))