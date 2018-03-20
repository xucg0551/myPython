# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']


    def make_requests_from_url(self, url):  #改写回调方法
        return scrapy.Request(url=url, callback=self.parse_index)

    def parse(self, response):
        pass

    def parse_index(self, response):
        self.logger.info('baidu', response.status)
