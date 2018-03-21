#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.error


#数据请求的两种方法

#第一种：没有构造Request对象
#第二种：构造Request对象

#第一种：没有构造Request对象

# urllib.request.urlopen(timeout=)

#get请求
# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.read().decode('utf8'))

#post请求
data = bytes(urllib.parse.urlencode({'word':'hello world'}),encoding='utf8')
# response = urllib.request.urlopen('http://httpbin.org/post', data=data)
# print(response.read().decode('utf8'))


#第二种：构造Request对象(重点)

#get请求
request = urllib.request.Request('https://python.org')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf8'))

#post请求，且带上请求头headers
dict = {
    'word':'hello world'
}
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
data = bytes(urllib.parse.urlencode(dict), encoding='utf8')
url = 'http://httpbin.org/post'
request = urllib.request.Request(url=url, headers=headers, method='POST', data=data)
# #也可以写成这样：
# request = urllib.request.Request(url=url, data=data, method='POST')
# request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
# request.add_header('Host', 'httpbin.org')

# response = urllib.request.urlopen(request)
# print(response.read().decode('utf8'))


#Handler 的用法
headers_handler = urllib.request.HTTPHandler(
    {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Host': 'httpbin.org'
    }
)
#
# proxies_handler = urllib.request.ProxyHandler({
#     'http': 'http://127.0.0.1:9743',
#     'https': 'https://127.0.0.1:9743'
# })
#
# url = 'http://httpbin.org/get'
# opener = urllib.request.build_opener(headers_handler)
# response = opener.open(url)
# print(response.read().decode('utf8'))

# proxy_handler = urllib.request.ProxyHandler({
#     'http': 'http://127.0.0.1:9743',
#     'https': 'https://127.0.0.1:9743'
# })
# opener = urllib.request.build_opener()
# opener.add_handler(headers_handler)
# urllib.request.install_opener(opener)
# # response = opener.open('http://httpbin.org/post', data=data)
# response = urllib.request.urlopen('http://httpbin.org/get')
# print(response.read().decode('utf8'))

#Cookie
import http.cookiejar

# #读取cookie
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# # response = opener.open('http://127.0.0.1:8080/')
# for item in cookie:
#     print(item.name+'='+item.value)

# #存储cookie
# filename = "cookie.txt"
# #两种格式的cookie MozillaCookieJar和LWPCookieJar
# cookie = http.cookiejar.MozillaCookieJar(filename)
# # cookie = http.cookiejar.LWPCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=True, ignore_expires=True)
#
# #请求带上cookie
# cookie = http.cookiejar.MozillaCookieJar()
# cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# print(response.read().decode('utf-8'))


# #异常处理
# try:
#     response = urllib.request.urlopen('http://www.baidu.com')
# except urllib.error.URLError as e:
#     if hasattr(e, 'code'):
#         print('code: ', e.code)
#     if hasattr(e, 'reason'):
#         print('reason: ', e.reason)
# except:  #没有全部列出来的异常，但是发生了异常，则在此处执行
#     print('what is now ....')
# else:  #没有异常的情况
#     print('Request Successfully')
# finally:
#     print('Request completed')





