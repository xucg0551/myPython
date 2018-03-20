#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

# def test():
#     yield 1
#     print(1)
#     yield 2
#     print(2)
#     yield 3
#     print(3)
#
# t = test()
# print(next(t))

def cash_out(amount):
    while amount > 0:
        amount -= 1
        yield 1
        print("擦，又来取钱了。。。败家子！")


ATM = cash_out(5)

print("取到钱 %s 万" % ATM.__next__())
print("花掉花掉!")
print("取到钱 %s 万" % ATM.__next__())
print("取到钱 %s 万" % ATM.__next__())
print("花掉花掉!")
print("取到钱 %s 万" % ATM.__next__())
print("取到钱 %s 万" % ATM.__next__())
print("取到钱 %s 万" % ATM.__next__())  # 到这时钱就取没了,再取就报错了
print("取到钱 %s 万" % ATM.__next__())