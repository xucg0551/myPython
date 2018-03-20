# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo




class DsfootballPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, **kwargs):
        self.mongo_uri = kwargs['mongo_uri']
        self.mongo_db = kwargs['mongo_db']
        self.collections = kwargs['collections']
        self.all_goals_dict = kwargs['all_goals_dict']
        self.let_goals_dict = kwargs['let_goals_dict']
        self.forbidden_list = kwargs['forbidden_list']

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            mongo_uri=settings.get('MONGO_URI'),
            mongo_db=settings.get('MONGO_DB'),
            collections = settings.get('COLLECTONS'),
            all_goals_dict=settings.get('ALL_GOALS_DICT'),
            let_goals_dict=settings.get('LET_GOALS_DICT'),
            forbidden_list=settings.get('FORBIDDENS_LI')
        )
        return cls(**params)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def process_item(self, item, spider):
        if '-' in item['all_goals']:  # 过滤掉没有大小球或让球的比赛
            return

        let_goals = abs(float(item['let_goals']))
        min_let_goals = self.let_goals_dict['min']
        max_let_goals = self.let_goals_dict['max']
        if (let_goals >= min_let_goals and let_goals <= max_let_goals) == False:
            return

        all_goals = float(item['all_goals'])
        min_all_goals = self.all_goals_dict['min']
        max_all_goals = self.all_goals_dict['max']
        if (all_goals >= min_all_goals and all_goals <= max_all_goals) == False:
            return

        for forbidden in self.forbidden_list:
            if forbidden in item['parties_name']:
                return

        self.db[self.collections].save(item)



    def close_spider(self, spider):
        self.client.close()