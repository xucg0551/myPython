#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import multiprocessing
import time

def counter():
    i = 0
    for _ in range(500000000):
        i = i + 1

    return True

def main():
    start_time = time.time()
    process_list = []

    for i in range(2):
        print(i)
        p = multiprocessing.Process(target=counter)
        p.start()
        process_list.append(p)
        # p.join()

    for p in process_list:
        p.join()

    print('{}'.format(time.time()-start_time))

main()