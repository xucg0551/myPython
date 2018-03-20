#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import queue, threading
import time, random

# q = queue.Queue(5)
#
# q.put(10)
# q.put(20)
# print(q.get())
# q.task_done()
# print(q.get())
# q.task_done()
#
# q.join()  #需要配合task_done

q = queue.Queue()

def producer():
    count = 0
    while True:
        print('producing......')
        time.sleep(random.randrange(3))
        q.put(count)
        count += 1

def consumer(name):
    while True:
        time.sleep(random.randrange(4))
        if not q.empty():
            data = q.get()
            print('{} is consuming {}'.format(name, data))
        else:
            print('no food')

p = threading.Thread(target=producer)
c1 = threading.Thread(target=consumer, args=('consumer 1', ))
c2 = threading.Thread(target=consumer, args=('consumer 2', ))
p.start()
c1.start()
c2.start()