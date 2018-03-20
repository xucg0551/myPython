#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import threading
import time

# def counter():
#     i = 0
#     for _ in range(500000000):
#         i = i + 1
#
#     return True
#
#
# def main():
#     start_time = time.time()
#     thread_list = []
#     for i in range(2):
#         print(i)
#         t = threading.Thread(target=counter)
#         t.start()
#         thread_list.append(t)
#         #t.join()   #注意：写在这里表示串行
#
#     for t in thread_list:
#         t.join()
#
#     print('{}'.format(time.time()-start_time))
#
# main()


# #通过线程类实现
# class MyThread(threading.Thread):
#     def __init__(self, num):
#         # threading.Thread.__init__(self)
#         super(MyThread, self).__init__()
#         self.num = num
#
#     def run(self):
#         print('running on number:{}'.format(self.num))
#         time.sleep(3)
#
# t1 = MyThread(56)
# t2 = MyThread(78)
#
# t1.start()
# # t1.join()
# t2.start()

#dead_lock
lock_a = threading.RLock()
lock_b = threading.RLock()

class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        self.func1()
        self.func2()

    def func1(self):
        lock_a.acquire()
        print('func1 get lock_a')
        lock_b.acquire()
        print('func1 get lock_b')
        lock_b.release()
        lock_a.release()

    def func2(self):
        lock_b.acquire()
        print('func2 get lock_b')
        time.sleep(0.1)
        lock_a.acquire()
        print('func2 get lock_a')
        lock_a.release()
        lock_b.release()

t1 = MyThread()
t2 = MyThread()
t1.start()
t2.start()
