#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
import sys

# print(sys.getdefaultencoding())
#
# str = '张三丰'  #str类型 为unicode编码
#
# str_to_utf8 = str.encode('utf-8') #unicode编码为utf-8
# print('utf-8:', str_to_utf8)
# # print(len(str))
# # print(len(str_to_utf8))
# # # print(bytes(str, encoding='utf-8'))
# # print(str_to_utf8.decode('utf-8'))
#
# str_to_gbk = str.encode('gbk')
# print('gbk:', str_to_gbk)
#
# str_to_gb2312 = str.encode('gb2312')
# print('gb2312:', str_to_gb2312)
#
# gbk_to_utf8 = str_to_gbk.decode('gbk').encode('utf-8')
# print('utf-8:',gbk_to_utf8)

# print(ord('老'))
# print(bin(ord('老')))
# sss = '老'.encode('gbk')
# print(sss)

s1 = '这是一个测试'
# print(type(str))
# str_2_gbk = str.encode('gbk')
# print(type(str_2_gbk))
# print(str_2_gbk)
#
str_2_utf8 = s1.encode('utf-8')

print(type(str_2_utf8))
print(str_2_utf8)
print(str(str_2_utf8,'utf8'))

# with open('xxx.txt', 'wb') as f:
#     f.write(str.encode('utf-8'))
#
#
# with open('xxx.txt', 'rb') as f:
#     ssss = f.read()
#     print(ssss)
#     print(ssss.decode('utf-8'))

# s2 = bytes(s1, 'utf-8')
# print(s2)




