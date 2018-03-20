# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # code = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
    latest_price = scrapy.Field()
    lowest_price = scrapy.Field()
    highest_price = scrapy.Field()
    up_down_percent = scrapy.Field()
    up_down_amount = scrapy.Field()
    deal_volume = scrapy.Field()
    deal_amount = scrapy.Field()
    open_price = scrapy.Field()
    close_price = scrapy.Field()
