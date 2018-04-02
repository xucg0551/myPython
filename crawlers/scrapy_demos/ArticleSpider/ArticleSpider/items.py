# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from models.es_types import ArticleType
import redis
from elasticsearch_dsl.connections import connections
es = connections.create_connection(ArticleType._doc_type.using)

redis_cli = redis.StrictRedis()


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+'-jobbole'


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_nums(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, params={'filter':["lowercase"], 'analyzer': 'ik_max_word'}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
            used_words = anylyzed_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor = MapCompose(add_jobbole)
        # input_processor = MapCompose(lambda x: x+'-jobbole')
    )
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
        # output_processor = TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=Join(',')
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    content = scrapy.Field()

    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.create_date = self['create_date']
        article.content = remove_tags(self['content'])
        article.front_image_url = self['front_image_url']
        if 'front_image_path' in self:
            article.front_image_path = self['front_image_path']
        article.praise_nums = self['praise_nums']
        article.comment_nums = self['comment_nums']
        article.fav_nums = self['fav_nums']
        article.url = self['url']
        article.tags = self['tags']
        article.meta.id = self['url_object_id']
        article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))

        redis_cli.incr('jobbole_count')
        article.save()

def remove_splash(value):
    return value.replace('/','')

def handle_address(value):
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip() != '查看地图']
    return ''.join(addr_list)

class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor = MapCompose(remove_splash)
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(remove_splash)
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash)
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(',')
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_address)
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need, job_type,
             publish_time, tags, job_advantage, job_desc, job_addr, company_url, company_name, crawl_time) 
             values(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s) 
             on duplicate key update salary=values(salary), job_desc=values(job_desc)
        '''
        params = (self['title'], self['url'], self['url_object_id'], self['salary'], self['job_city'], self['work_years'],
                  self['degree_need'], self['job_type'], self['publish_time'], self['tags'], self['job_advantage'], self['job_desc'],
                  self['job_addr'], self['company_url'], self['company_name'], self['crawl_time'].strftime('%Y-%m-%d %H:%M:%S'))

        return insert_sql, params


