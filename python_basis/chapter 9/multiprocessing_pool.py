#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import time

def foo(args):
    time.sleep(1)
    print(args)


p = Pool(5)
for i in range(30):
    p.apply_async(func=foo, args=(i, ))
p.close()
p.join()