#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import requests, json


#请求

# #基本GET请求
# response = requests.get('http://www.baidu.com')
# print(response.text)

# #带参数GET请求
# response = requests.get('http://httpbin.org/get?name=germey&age=22')
# print(response.text)

# #参数为字典
# data = {
#     'name': 'zhangsan',
#     'age': 22
# }
# response = requests.get('http://httpbin.org/get', params=data)
# print(response.text)

# #解析json
# response = requests.get('http://httpbin.org/get')
# print(type(response.text))
# print(type(response.json()))
# print(response.json())
# #也可以用json.loads()反序列化
# print(json.loads(response.text))

# #获取二进制数据
# response = requests.get('https://github.com/favicon.ico')
# # with open('favicon.ico', 'wb') as f:
# #     f.write(response.content)
# print(type(response.text))
# print(type(response.content))
# print(response.text)
# print(response.content)

# #添加headers
# response = requests.get("https://www.zhihu.com/explore")
# print(response.text)
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
# }
# response = requests.get("https://www.zhihu.com/explore", headers=headers)
# print(response.text)

# #基本POST请求
# data = {'name': 'germey', 'age': '22'}
# response = requests.post("http://httpbin.org/post", data=data)
# print(response.text)
#
# data = {'name': 'germey', 'age': '22'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
# response = requests.post("http://httpbin.org/post", data=data, headers=headers)
# print(response.json())


# #文件上传
# files = {'file': open('favicon.ico', 'rb')}
# print(files)
# response = requests.post("http://127.0.0.1:8080/file/", files=files)
# print(response.text)

# #获取cookie
# response = requests.get("http://127.0.0.1:8080/cookie/")
# print(response.cookies)
# for key, value in response.cookies.items():
#     print(key + '=' + value)

#模拟登陆(session，很重要)
s = requests.Session()
response = s.get('http://127.0.0.1:8080/cookie/')   #获取登陆成功后返回的cookies，s就会自动携带cookie进行后面的操作
print(response.cookies)
response = s.get('http://127.0.0.1:8080/session/')
print(response.text)
print(response.cookies)

# requests.get('http://127.0.0.1:8080/cookie/')

# # #代理设置
# proxies = {
#   "http": "http://120.205.70.102:8060",
#   "https": "https://120.205.70.102:8060",
# }
#
# response = requests.get("http://127.0.0.1:8080/cookie/", headers=headers, timeout=20)
# print(response.text)
# print(response.status_code)

# #异常处理
# from requests.exceptions import ReadTimeout, ConnectionError, RequestException
# try:
#     response = requests.get("http://httpbin.org/get", timeout = 0.5)
#     print(response.status_code)
# except ReadTimeout:
#     print('Timeout')
# except ConnectionError:
#     print('Connection error')
# except RequestException:
#     print('Error')