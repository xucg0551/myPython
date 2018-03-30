#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-


from  _datetime import datetime
from random import random
import json


# 生成随机数文件
def dump_random_array(file = 'numbers.json', size = 10 ** 5):
    with open(file, 'w') as f:
        numlst = list()
        for i in range(size):
            numlst.append(int(random() * 10 ** 6))
        json.dump(numlst, f)

    # with open(file, 'w') as f:
    #     numlst = list()
    #     for i in range(size):
    #         numlst.append(int(random() * 10 ** 10))
    #     f.write(json.dumps(numlst))

#加载随机数列表
def load_random_array(file = 'numbers.json'):
    with open(file, 'r') as f:
        return json.load(f)
        # numlst = f.read()
        # return json.loads(numlst)



# 显示函数执行时间
def exectime(func):
    def inner(*args, **kwargs):
        begin = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        inter = end - begin
        print('E-time:{0}.{1}'.format(
            inter.seconds,
            inter.microseconds
        ))
        return result
    return inner



#快速排序
@exectime
def quick_sort(array):
    def recursive(begin, end):
        if begin > end:
            return
        l, r = begin, end
        pivot = array[l]
        while l < r:
            while l < r and array[r] > pivot:
                r -= 1
            while l < r and array[l] <= pivot:
                l += 1
            array[l], array[r] = array[r], array[l]
        array[l], array[begin] = pivot, array[l]
        recursive(begin, l - 1)
        recursive(r + 1, end)

    recursive(0, len(array) - 1)
    return array

# #传说中的三行代码  代码缺陷是会开辟新的空间
# def quick_sort(arr):
#     if len(arr) < 2:
#         return arr
#     pivot = arr[0]
#     # 开辟新的空间  (增加空间复杂度)
#     less = [i for i in arr[1:] if i < pivot]
#     greater = [i for i in arr[1:] if i >= pivot]
#
#     return quick_sort(less) + [pivot] + quick_sort(greater)


if __name__ == '__main__':
    # dump_random_array()
    datas = load_random_array()
    # quick_sort(datas)
    # print(quick_sort(datas))
    i = 3
    j = 5
    print(i, j)
    i, j = j, i
    print(i, j)



