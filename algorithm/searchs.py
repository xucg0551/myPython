#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

#无序查找  O(n)
def sequential_search(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    else:
        return False


#有序查找
#1.二分查找  O(log(n))
def binary_search(arr, key):
    low = 0
    high = len(arr) - 1
    time = 0
    while low < high:
        time += 1
        mid = (low + high) // 2;
        if key > arr[mid]:
            low = mid -1
        elif key < arr[mid]:
            high = mid + 1
        else:
            print("times: %s" % time)
            return mid
    print("times: %s" % time)
    return -1

#二分递归实现
def binary_search2(arr, key, low, high):
    mid = low + ( high-low ) // 2

    if(arr[mid] == key):
        return mid
    if(arr[mid]> key):
        return binary_search2(arr, key, low, mid-1)
    if(arr[mid] < key):
        return binary_search2(arr, key, mid+1, high)


#2.插值查找 二分查找的改进版本  其优点是，对于表内数据量较大，且关键字分布比较均匀的查找表，使用插值算法的平均性能比二分查找要好得多。反之，对于分布极端不均匀的数据，则不适合使用插值算法。
def interpolation_search(arr, key):
    low = 0
    high = len(arr) - 1
    time = 0
    while low < high:
        time += 1
        # 计算mid值是插值算法的核心代码
        mid = low + int((high - low) * (key - arr[low]) / (arr[high] - arr[low]))
        print("mid=%s, low=%s, high=%s" % (mid, low, high))
        if key < arr[mid]:
            high = mid - 1
        elif key > arr[mid]:
            low = mid + 1
        else:
            # 打印查找的次数
            print("times: %s" % time)
            return mid
    print("times: %s" % time)
    return -1

#3.哈希查找
    # 散列函数是否均匀
    # 处理冲突的办法
    # 散列表的装填因子（表内数据装满的程度）


class HashTable(object):
    def __init__(self, size):
        self.elements = [None for i in  range(size)]
        self.count = size

    def hash(self, key):
        return key % self.count

    def insert(self, key):
        address = self.hash(key)
        while self.elements[address]:
            address = (address+1) % self.count
        self.elements[address] = key

    def search(self, key):
        start = address = self.hash(key)
        while self.elements[address] != key:
            address = (address+1) % self.count
            if not self.elements[address] or address == start:
                return False
        return True



if __name__ == '__main__':
    # LIST = [1, 5, 8, 123, 22, 54, 7, 99, 300, 222]
    # result = sequential_search(LIST, 123)

    # LIST = [1, 5, 7, 8, 22, 54, 99, 123, 200, 222, 444]
    # # result = binary_search(LIST, 99)
    # result = binary_search2(LIST, 99, 0, len(LIST))
    # # result = interpolation_search(LIST, 99)
    # print(result)

    list_a = [12, 67, 56, 16, 25, 37, 22, 29, 15, 47, 48, 34]
    ht = HashTable(12)
    for i in list_a:
        ht.insert(i)

    for i in ht.elements:
        if i:
            print((i, ht.elements.index(i)), end=" ")
    print("\n")

    print(ht.search(15))
    print(ht.search(33))