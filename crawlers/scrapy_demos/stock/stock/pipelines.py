# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import hashlib
import pymongo
from scrapy.exceptions import DropItem
from collections import defaultdict


K_LINE = 'k_line'

class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.stocks = defaultdict(dict)

    @classmethod
    def from_crawler(cls, cralwer):  #获取全局配置，也可以放在spider里面
        return cls(
            mongo_uri=cralwer.settings.get('MONGO_URI'),
            mongo_db=cralwer.settings.get('MONGO_DB')
        )
    # @classmethod  #也可以通过from_settings获取配置信息
    # def from_settings(cls, settings):
    #     return cls(
    #         mongo_uri=settings.get('MONGO_URI'),
    #         mongo_db=settings.get('MONGO_DB')
    #     )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        #获取数据库中所有的股票信息
        for item in self.db[K_LINE].find():
            self.stocks[item['_id']] = item

    def process_item(self, item, spider):
        code = item['_id']
        stock = self.stocks[code] if code in self.stocks else defaultdict(list)  # 使用defaultdict防止keyError抛出

        # 填充数据
        stock['_id'] = code
        stock['link'] = item['link']
        stock['name'] = item['name']

        stock['latest_prices'].append(item['latest_price'])
        stock['up_down_percents'].append(item['up_down_percent'])
        stock['up_down_amounts'].append(item['up_down_amount'])
        stock['deal_volumes'].append(item['deal_volume'])
        stock['deal_amounts'].append(item['deal_amount'])
        stock['open_prices'].append(item['open_price'])
        stock['close_prices'].append(item['close_price'])
        stock['lowest_prices'].append(item['lowest_price'])
        stock['highest_prices'].append(item['highest_price'])

        # 插入数据库
        self.db[K_LINE].save(stock)
        return item

    def close_spider(self, spider):
        self.client.close()





