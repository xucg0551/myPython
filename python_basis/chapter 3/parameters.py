#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-


#位置参数和命名参数
def test(x, y, z):
    print(x)
    print(y)
    print(z)

# test(y = 1, x = 2, z = 3)
# test(2, y = 3, 4)  #命名参数必须放在位置参数后面
# test(2, 3, y=4)  #位置参数3已经赋值给y了，y=4的命名参数又赋值给y，则会出错


# def test1(*args):
#     print(args)
#     a, b, c = args
#     #print(a)
#     # print(b)
#     # print(c)
#
# # test1('a', 'b', 'c')
# test1('a')

# def test2(x,y, **kwargs):
#     print(x)
#     print(y)
#     print(kwargs)
#
# test2(y=4, z=5, x=6, a=7)

def test3(x, y, z=9,  *args, **kwargs):
    print(x)
    print(y)
    print(z)
    print(args)
    print(kwargs)

test3(1, 2, 3, 4, 5, a=6, b=7)