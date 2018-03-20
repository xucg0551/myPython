#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

# capitalize()将字符串的第一个字母变成大写,其他字母变小写。该方法返回一个首字母大写的字符串
a_str = 'aBc, D'
print(a_str.capitalize())

# center() 返回一个原字符串居中,并使用空格填充至长度 width 的新字符串。默认填充字符为空格。
b_str = 'python'
print(b_str.center(20))
print(b_str.center(20, '*'))

# count() 方法用于统计字符串里某个字符出现的次数。可选参数为在字符串搜索的开始与结束位置。
c_str = "this is string example....wow!!!";
print(c_str.count('i', 4, 40))
print(c_str.count('wow'))

#encode() decode()
d_str = 'this is string example....wow!!!'
str_encode = d_str.encode('utf-8', 'strict')
print(str_encode.decode('utf-8', 'strict'))

#startswith() 方法用于检查字符串是否是以指定子字符串开头，如果是则返回 True，否则返回 False。如果参数 beg 和 end 指定值，则在指定范围内检查
# endswith() 方法用于判断字符串是否以指定后缀结尾，如果以指定后缀结尾返回True，否则返回False。可选参数"start"与"end"为检索字符串的开始与结束位置。
e_str = "this is string example....wow!!!"
print(e_str.startswith('this'))
print(e_str.startswith('is', 2, 4))

f_str = "this is string example....wow!!!"
print(f_str.endswith('wow!!!'))
print(f_str.endswith('is', 2, 4))
print(f_str.endswith('is', 2, 6))


#isalnum() 方法检测字符串是否由字母和数字组成
g_str = 'this2018'
print(g_str.isalnum())

#isalpha() 方法检测字符串是否只由字母组成
h_str = 'this'
print(h_str.isalpha())
h_str = 'this is string example....wow!!!'
print(h_str.isalpha())

#isdigit() 方法检测字符串是否只由数字组成
i_str = '123456'
print(i_str.isdigit())
i_str = '12345f'
print(i_str.isdigit())

# isupper() 方法检测字符串中所有的字母是否都为大写
# islower() 方法检测字符串是否由小写字母组成

# istitle() 方法检测字符串中所有的单词拼写首字母是否为大写，且其他字母为小写
j_str = "This Is String Example...Wow!!!"
print(j_str.istitle())

j_str = "This is string example....wow!!!"
print(j_str.istitle())