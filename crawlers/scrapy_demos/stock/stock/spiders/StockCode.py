# -*- coding: utf-8 -*-
import scrapy
from stock.items import StockItem


#scrapy crawl stocks --nolog  -o stock.json -s FEED_EXPORT_ENCODING=utf-8  生成中文的json文件

class StockcodeSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['ifeng.com']
    # start_urls = ["http://app.finance.ifeng.com/list/stock.php?t=ha&f=symbol&o=asc&p=1",
    #               "http://app.finance.ifeng.com/list/stock.php?t=sa&f=symbol&o=asc&p=1"]
    start_urls = ["http://app.finance.ifeng.com/list/stock.php?t=ha",
                  "http://app.finance.ifeng.com/list/stock.php?t=sa"]

    def __init__(self, mongo_uri, mongo_db, *args, **kwargs):
        super(StockcodeSpider, self).__init__(*args, **kwargs)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, cralwer):  # 获取全局配置，也可以放在spider里面
        return cls(
            mongo_uri=cralwer.settings.get('MONGO_URI'),
            mongo_db=cralwer.settings.get('MONGO_DB')
        )

    def parse(self, response):
        for item in response.xpath('//*[@class= "tab01"]/table//tr[position()>1]')[:-1]:
            stock = StockItem()
            link = item.xpath('td[2]/a/@href').extract_first()
            code = item.xpath('td[1]/a/text()').extract_first()  #股票代码
            name = item.xpath('td[2]/a/text()').extract_first()  #股票名称
            latest_price = item.xpath('td[3]/span/text()').extract_first()    #最新价
            up_down_percent = item.xpath('td[4]/span/text()').re_first('(.*?)%') #涨跌幅
            up_down_amount = item.xpath('td[5]/span/text()').extract_first()  #涨跌额
            deal_volume = item.xpath('td[6]/text()').re_first('(\d+)')     #成交量
            deal_amount = item.xpath('td[7]/text()').re_first('(\d+)')     #成交额
            open_price = item.xpath('td[8]/span/text()').extract_first()      #今开盘
            close_price = item.xpath('td[9]/text()').extract_first()          #昨收盘
            lowest_price = item.xpath('td[10]/span/text()').extract_first()   #最低价
            highest_price = item.xpath('td[11]/span/text()').extract_first()  #最高价

            stock['_id'] = code
            stock['name'] = name
            stock['link'] = link
            stock['latest_price'] = float(latest_price)
            stock['up_down_percent'] = float(up_down_percent)
            stock['up_down_amount'] = float(up_down_amount)
            stock['deal_volume'] = float(deal_volume)
            stock['deal_amount'] = float(deal_amount)
            stock['open_price'] = float(open_price)
            stock['close_price'] = float(close_price)
            stock['lowest_price'] = float(lowest_price)
            stock['highest_price'] = float(highest_price)
            yield stock

        # yield scrapy.Request(response.url, callback=self.parse_page)

        next = response.xpath('//*[@class= "tab01"]/table/tr[last()]/td/a[last()]/@href').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url, callback=self.parse)

    def parse_page(self, response):
        for item in response.xpath('//*[@class= "tab01"]/table//tr[position()>1]')[:-1]:
            stock = StockItem()
            link = item.xpath('td[2]/a/@href').extract_first()
            code = item.xpath('td[1]/a/text()').extract_first()  #股票代码
            name = item.xpath('td[2]/a/text()').extract_first()  #股票名称
            latest_price = item.xpath('td[3]/span/text()').extract_first()    #最新价
            up_down_percent = item.xpath('td[4]/span/text()').re_first('(.*?)%') #涨跌幅
            up_down_amount = item.xpath('td[5]/span/text()').extract_first()  #涨跌额
            deal_volume = item.xpath('td[6]/text()').re_first('(\d+)')     #成交量
            deal_amount = item.xpath('td[7]/text()').re_first('(\d+)')     #成交额
            open_price = item.xpath('td[8]/span/text()').extract_first()      #今开盘
            close_price = item.xpath('td[9]/text()').extract_first()          #昨收盘
            lowest_price = item.xpath('td[10]/span/text()').extract_first()   #最低价
            highest_price = item.xpath('td[11]/span/text()').extract_first()  #最高价

            stock['_id'] = code
            stock['name'] = name
            stock['link'] = link
            stock['latest_price'] = float(latest_price)
            stock['up_down_percent'] = float(up_down_percent)
            stock['up_down_amount'] = float(up_down_amount)
            stock['deal_volume'] = float(deal_volume)
            stock['deal_amount'] = float(deal_amount)
            stock['open_price'] = float(open_price)
            stock['close_price'] = float(close_price)
            stock['lowest_price'] = float(lowest_price)
            stock['highest_price'] = float(highest_price)
            yield stock
