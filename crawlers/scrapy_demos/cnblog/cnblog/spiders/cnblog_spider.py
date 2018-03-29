# -*- coding: utf-8 -*-
import scrapy
from cnblog.items import CnblogItem


class CnblogSpider(scrapy.Spider):
    name = 'cnblog_spider'
    allowed_domains = ['cnblogs.com']
    start_urls = [
        "http://www.cnblogs.com/qiyeboy/default.html?page=1"
    ]

    custom_settings = {
        'ITEM_PIPELINES':{
                    'cnblog.pipelines.CnblogPipeline': 300,
                    'cnblog.pipelines.MyImagePipeline':1,
        }
    }

    # def start_requests(self):
    #     yield scrapy.Request('http://httpbin.org/post',method='POST', callback=self.test_post)
    #
    # def test_post(self, response):
    #     pass

    def parse(self, response):
        articles = response.xpath(".//*[@class='day']")

        # #在shell中进行调试  ctrl+D可以恢复    妙！！！
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        # 从每篇文章中抽取数据
        for article in articles:
            url = article.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = article.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            # time = article.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            # content = article.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogItem(title=title)
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_body)

        # next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        # if next_page:
        #     yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['image_urls'] = body.xpath('.//img//@src').extract()  # 提取图片链接
        yield item
