#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import hashlib

hash = hashlib.md5()
hash.update('这是一个测试'.encode('gbk'))
print(hash.hexdigest())
print(hash.digest())