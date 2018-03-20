# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass

    def start_requests(self):
       return [scrapy.Request(url='https://www.zhihu.com/signup?next=%2F', callback=self.login)]

    def login(self, response):
        print(response.text)

