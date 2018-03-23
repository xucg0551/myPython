#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

# class UpperAttrMetaclass(type):
#
#     def __new__(cls, clsname, bases, attrs):
#         print('UpperAttrMetaclass')
#         uppercase_attr = {}
#         for name, val in attrs.items():
#             print('key={},val={}'.format(name, val))
#             if not name.startswith('__'):
#                 uppercase_attr[name.upper()] = val
#             else:
#                 uppercase_attr[name] = val
#         print(uppercase_attr)
#         return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr)
#
#
# class Test(object, metaclass=UpperAttrMetaclass):
#     cls_val = 1
#     def __init__(self, name):
#         print('ttttttttttttttttttt')
#         self.name = name
#
#     def __new__(cls, *args, **kwargs):
#         print('fsdafafafsafa')
#
#
# t = Test(name='fasdfasfasdfs')
# print(Test.CLS_VAL)

class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_ip181(self):
        pass
        # start_url = 'http://www.ip181.com/'
        # html = get_page(start_url)
        # ip_adress = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        # # \s* 匹配空格，起到换行作用
        # re_ip_adress = ip_adress.findall(html)
        # for adress,port in re_ip_adress:
        #     result = adress + ':' + port
        #     yield result.replace(' ', '')


    def crawl_xicidaili(self):
        pass
        # for page in range(1, 4):
        #     start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
        #     html = get_page(start_url)
        #     ip_adress = re.compile('<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        #     # \s* 匹配空格，起到换行作用
        #     re_ip_adress = ip_adress.findall(html)
        #     for adress, port in re_ip_adress:
        #         result = adress+':'+ port
        #         yield result.replace(' ', '')

    def crawl_ip3366(self):
        pass
        # for page in range(1, 4):
        #     start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
        #     html = get_page(start_url)
        #     ip_adress = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        #     # \s * 匹配空格，起到换行作用
        #     re_ip_adress = ip_adress.findall(html)
        #     for adress, port in re_ip_adress:
        #         result = adress+':'+ port
        #         yield result.replace(' ', '')


f = FreeProxyGetter()
print(dir(f))
print(f.__CrawlFuncCount__)
