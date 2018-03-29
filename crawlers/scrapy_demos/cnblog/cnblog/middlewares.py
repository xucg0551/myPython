# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import requests



class CnblogSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#User-Agent中间件
class RandomUserAgentMiddleware(object):

    def __init__(self, ua_type):
        self.ua = UserAgent()
        self.ua_type = ua_type

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['USER_AGENT_TYPE'])  #settings 中的key一定要大写吗 ？

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault(b'User-Agent', get_ua())

#IP代理中间件
class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        proxies = requests.get('http://127.0.0.1:5000/get')
        proxies = 'http://' + proxies.content.decode()
        request.meta['proxy'] = proxies


from scrapy.http import HtmlResponse
class JSPageProxyMiddleware(object):

    # def __init__(self):
    #     self.browser = webdriver.Chrome()
    #     super(JSPageProxyMiddleware, self).__init__()

    def process_request(self, request, spider):
        # if request.url
        if spider.name == 'cnblog_spider':
            spider.browser.get(request.url)
            import time
            # time.sleep(3)
            print('visiting {0}'.format(request.url))
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf-8', request=request)


