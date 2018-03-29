#模拟登录和自动爬取的实现

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from faker import Factory

f = Factory.create()

class GithubSpider(CrawlSpider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/']

    rules = (
        # 消息列表
        Rule(LinkExtractor(allow=('/xucg0551/.*',),restrict_xpaths='//ul[@class="mini-repo-list"]/li'),
             callback='parse_page'),
        # # 下一页, If callback is None follow defaults to True, otherwise it defaults to False
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="next_page"]')),
    )

    post_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": f.user_agent(),
        "Referer": "https://github.com/",
    }

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        return [scrapy.Request(url = "https://github.com/login",
                               meta = {'cookiejar': 1},
                               callback = self.post_login)]

    def post_login(self, response):
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        self.logger.info('authenticity_token=' + authenticity_token)
        form_data = {
            'commit': 'Sign+in',
            'utf8': '✓',
            'login': 'xcg19865@126.com',
            'password': 'jhjh159',
            'authenticity_token': authenticity_token
        }

        self.logger.info('form_data={}'.format(form_data))
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数，如果url跟Request页面的一样就省略掉
        return [scrapy.FormRequest.from_response(response,
                                          url='https://github.com/session',
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.post_headers,  # 注意此处的headers
                                          formdata=form_data,
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]

    def after_login(self, resopnse):
        for url in self.start_urls:
            yield scrapy.Request(url, meta = {'cookiejar': resopnse.meta['cookiejar']})

    def parse_page(self, response):
        """这个是使用LinkExtractor自动处理链接以及`下一页`"""
        self.logger.info(u'--------------消息分割线-----------------')
        self.logger.info(response.url)
