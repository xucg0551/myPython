# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path
        return item

class MysqlPipeline(object):
    #采用同步机制
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'jhjh159@', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
        insert into jobbole_article(title, url, create_date, fav_nums, url_object_id) values(%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums'], item['url_object_id']))
        self.conn.commit()

class MysqlTwistedPipeline(object):
    #异步机制
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            passwd = settings['MYSQL_PASSWORD'],
            user = settings['MYSQL_USER'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  #处理异常

    #处理异步插入的异常
    def handle_error(self,failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
        # insert_sql = """
        #         insert into jobbole_article(title, url, create_date, fav_nums, url_object_id) values(%s, %s, %s, %s, %s)
        #         """
        # cursor.execute(insert_sql,(item['title'], item['url'], item['create_date'], item['fav_nums'], item['url_object_id']))






