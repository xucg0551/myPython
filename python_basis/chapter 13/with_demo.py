#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-


#第一种方法
from contextlib import contextmanager
@contextmanager
def my_open(path, mode):
    f = open(path, mode)
    yield f
    f.close()

#第二种方法
class My_Open(object):
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print('entering')
        self.f = open(self.filename, self.mode)
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('will exit')
        self.f.close()


if __name__ == '__main__':
    # with My_Open('aaa.text', 'w') as f:
    #     f.write('asffsafasddsa')

    with my_open('aaa.text', 'w') as f:
        f.write('12343')

    # with open('aaa.txt', 'r') as f:
    #     f.write('fdsafaf')


