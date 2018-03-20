#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

# from greenlet import greenlet
#
# def test1():
#     print(12)
#     gr2.switch()
#     print(34)
#     gr2.switch()
#
# def test2():
#     print(56)
#     gr1.switch()
#     print(78)
#
# gr1 = greenlet(test1)
# gr2 = greenlet(test2)
# gr1.switch()

# import gevent
# import time
#
# def foo():
#     print('running in foo')
#     gevent.sleep(2)
#     print('switch to foo again')
#
# def bar():
#     print('switch to bar')
#     gevent.sleep(5)
#     print('switch to bar again')
#
# start = time.time()
# gevent.joinall(
#     [gevent.spawn(foo),
#     gevent.spawn(bar)]
# )
#
# print(time.time()-start)

from urllib import request
import gevent,time
from gevent import monkey
monkey.patch_all() #把当前程序的所有的io操作给我单独的做上标记

def f(url):
    print('GET: %s' % url)
    resp = request.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))

urls = ['https://www.python.org/',
        'https://www.yahoo.com/',
        'https://github.com/' ]
time_start = time.time()
for url in urls:
    f(url)
print("同步cost",time.time() - time_start)
async_time_start = time.time()
gevent.joinall([
    gevent.spawn(f, 'https://www.python.org/'),
    gevent.spawn(f, 'https://www.yahoo.com/'),
    gevent.spawn(f, 'https://github.com/'),
])
print("异步cost",time.time() - async_time_start)

