#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
import threading
import time

# def worker(event):
#     while not event.is_set():
#         print('waitting...')
#         event.wait()
#     print('event is ready')
#
#
# redis_event = threading.Event()
# t1 = threading.Thread(target=worker, args=(redis_event, ))
# t2 = threading.Thread(target=worker, args=(redis_event, ))
#
# t1.start()
# t2.start()
#
# time.sleep(3)
# redis_event.set()

def producer(event):
    while True:
        time.sleep(1)
        print('food is ready...')
        event.set()

def consumer(event):
    while True:
        if not event.is_set():
            event.wait()
        else:
            print('consume food...')
            time.sleep(3)
            event.clear()

event = threading.Event()
p = threading.Thread(target=producer, args=(event, ))
c = threading.Thread(target=consumer, args=(event, ))

p.start()
c.start()





