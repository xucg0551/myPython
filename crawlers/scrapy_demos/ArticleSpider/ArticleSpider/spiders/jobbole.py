# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
from scrapy import Request
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #获取当前页面的文章链接并请求数据
        # post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first('')
            image_url = post_node.css('img::attr(src)').extract_first('')
            yield Request(response.urljoin(post_url),meta={'front_image_url': image_url} ,callback=self.parse_detail)

        #获取下一面的链接并请求数据
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield  Request(response.urljoin(next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()

        front_image_url = response.meta.get('front_image_url', '')  #文章封面图
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        title = response.css('.entry-header h1::text').extract_first()

        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace('·', '')
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract_first().strip().replace('·', '').strip()

        try:
            create_date = dt.datetime.strptime(create_date, '%Y/%m/%d')
        except Exception as e:
            create_date = dt.datetime.now().date()

        # praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]//h10/text()').extract_first()
        praise_nums = response.css('.vote-post-up h10::text').extract_first()

        fav_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').re_first(('\d+'))
        # fav_nums = response.css('.bookmark-btn::text').re_frist(('\d+'))  //有问题

        comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').re_first(('\d+'))
        # comment_nums = response.css('a[href="#article-comment"] span::text').re_first(('\d+'))  //有问题

        # content = response.xpath('//div[@class="entry"]').extract_first()
        content = response.css('div.entry').extract_first()

        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ','.join(tag_list)

        article_item['title'] = title
        article_item['url'] = response.url
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['comment_nums'] = comment_nums
        article_item['fav_nums'] = fav_nums
        article_item['tags'] = tags
        article_item['content'] = content
        article_item['url_object_id'] = get_md5(response.url)

        #通过item loader加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('create_date', 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_xpath('comment_nums', '//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath('fav_nums', '//span[contains(@class, "bookmark-btn")]/text()')
        item_loader.add_css('tags', 'p.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content', 'div.entry')

        article_item = item_loader.load_item()

        yield article_item
