# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DsfootballItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parties_name = scrapy.Field()
    all_goals = scrapy.Field()
    let_goals = scrapy.Field()
    _id = scrapy.Field()
    # time = scrapy.Field()
    pass
