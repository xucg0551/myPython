# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class HefeiSpider(scrapy.Spider):
    name = 'hefei'
    allowed_domains = ['news.hefei.cc']
    start_urls = ['http://news.hefei.cc/L/12020100.shtml']

    #1.解析当前页面的所有新闻的url
    #2.解析下一页的url，且请求数据，循环请求
    def parse(self, response):
        #解析当前页的所有url并请求
        nodes = response.css('div.list_left ul li')
        for node in nodes:
            url = node.css('li a::attr(href)').extract_first()
            title = node.css('li a::attr(title)').extract_first()
            # yield Request(response.urljoin(url), callback=self.parse_detail)

        #解析下一页并请求
        next = response.xpath("//a[@class='p_redirect'][last()]/@href").extract_first()
        if next:
            next_url = response.urljoin(next)
            # print(next_url)
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        # print(response.url)
        pass
