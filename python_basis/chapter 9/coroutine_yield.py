#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import time

"""
传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。
如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高。
"""


# 注意到consumer函数是一个generator（生成器）:
# 任何包含yield关键字的函数都会自动成为生成器(generator)对象

def consumer():
    r = ''
    while True:
        # 3、consumer通过yield拿到消息，处理，又通过yield把结果传回；
        #    yield指令具有return关键字的作用。然后函数的堆栈会自动冻结(freeze)在这一行。
        #    当函数调用者的下一次利用next()或generator.send()或for-in来再次调用该函数时，
        #    就会从yield代码的下一行开始，继续执行，再返回下一次迭代结果。通过这种方式，迭代器可以实现无限序列和惰性求值。
        time.sleep(10)
        n = yield r
        if not n:
            return
        print('[CONSUMER] ←← Consuming %s...' % n)
        time.sleep(1)
        r = '200 OK'


def produce(c):
    # 1、首先调用c.next()启动生成器
    next(c)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] →→ Producing %s...' % n)
        # 2、然后，一旦生产了东西，通过c.send(n)切换到consumer执行；
        cr = c.send(n)
        # 4、produce拿到consumer处理的结果，继续生产下一条消息；
        print('[PRODUCER] Consumer return: %s' % cr)
    # 5、produce决定不生产了，通过c.close()关闭consumer，整个过程结束。
    c.close()


if __name__ == '__main__':
    # 6、整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。
    c = consumer()
    produce(c)
