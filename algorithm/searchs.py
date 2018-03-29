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
    return False

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
    return False



if __name__ == '__main__':
    # LIST = [1, 5, 8, 123, 22, 54, 7, 99, 300, 222]
    # result = sequential_search(LIST, 123)

    LIST = [1, 5, 7, 8, 22, 54, 99, 123, 200, 222, 444]
    # result = binary_search(LIST, 99)
    result = interpolation_search(LIST, 99)
    print(result)