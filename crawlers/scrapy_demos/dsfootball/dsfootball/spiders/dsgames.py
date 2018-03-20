# -*- coding: utf-8 -*-
import scrapy
import datetime
from dsfootball.items import DsfootballItem
from dsfootball.utils.common import get_md5


class DsgamesSpider(scrapy.Spider):
    name = 'dsgames'
    allowed_domains = ['www.dszuqiu.com']
    start_urls = ['https://www.dszuqiu.com/diary']


    def parse(self, response):
        trs = response.css('div#diary_info tbody tr')
        for tr in trs:
            item = DsfootballItem()
            all_goals = tr.xpath("td[contains(@class, 'text-center BR0')][last()]/a/text()").extract_first()
            let_goals = tr.xpath("td[contains(@class, 'text-center yellowTd BR0')][2]/a/text()").extract_first()
            parter_one_name = tr.xpath("td[contains(@class, 'text-right BR0')]/a/text()").extract_first().strip()
            parter_two_name = tr.xpath("td[contains(@class, 'text-left')]/a/text()").extract_first().strip()
            parties_name = '{} v {}'.format(parter_one_name, parter_two_name)
            item['all_goals'] = all_goals
            item['let_goals'] = let_goals
            item['parties_name'] = parties_name
            item['_id'] = get_md5(parties_name)
            # item['time'] = datetime.datetime.utcnow()
            yield item

