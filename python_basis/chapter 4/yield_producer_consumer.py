#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import time

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming {}...'.format(n))
        time.sleep(1)
        r = '200 OK'


def producer(c):
    next(c)   #启动生成器
    n = 0
    while n < 5:
        n += 1
        print('[PRODUCER] Producing {}...'.format(n))
        r = c.send(n)
        print('[PRODUCER] Consumer return: {}'.format(r))
    c.close()

c = consumer()
producer(c)