#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import whois


print(whois.query('http://www.baidu.com').__dict__)
# print(whois.query('http://www.baidu.com').name_servers)
