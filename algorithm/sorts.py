#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-


from  _datetime import datetime
from random import random
import json


# 生成随机数文件
def dump_random_array(file = 'numbers.json', size = 10 ** 6):
    with open(file, 'w') as f:
        numlst = list()
        for i in range(size):
            numlst.append(int(random() * 10 ** 7))
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
# def exectime(func):
#     def inner(*args, **kwargs):
#         begin = datetime.now()
#         result = func(*args, **kwargs)
#         end = datetime.now()
#         inter = end - begin
#         print('E-time:{0}.{1}'.format(
#             inter.seconds,
#             inter.microseconds
#         ))
#         return result
#     return inner

def exectime(type):
    def inner(func):
        def outter(*args, **kwargs):
            begin = datetime.now()
            result = func(*args, **kwargs)
            end = datetime.now()
            inter = end - begin
            print('{0}_time:{1}.{2}'.format(
                type,
                inter.seconds,
                inter.microseconds
            ))
            return result
        return outter
    return inner

#堆排序
def max_heapify(heap, heap_size, root):
    left_child = 2 * root + 1
    right_child = 2 * root + 2
    index = root
    if left_child < heap_size and heap[index] < heap[left_child]:
        index = left_child
    if right_child < heap_size and heap[index] < heap[right_child]:
        index = right_child
    if index != root:
        heap[index], heap[root] = heap[root], heap[index]
        max_heapify(heap, heap_size, index)

def build_max_heap(heap):  #构建最大堆
    heap_size = len(heap)
    for i in range((heap_size-2)//2, -1, -1):
        max_heapify(heap, heap_size, i)

@exectime('heap_sort')
def heap_sort(heap):#将根节点取出与最后一位做对调，对前面len-1个节点继续进行对调整过程。
    build_max_heap(heap)
    for i in range(len(heap)-1, -1, -1):
        heap[0], heap[i] = heap[i], heap[0]
        max_heapify(heap, i, 0)
    return heap



#快速排序
@exectime('quick_sort')
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
    quick_sort(datas)
    #
    heap_sort(datas)





