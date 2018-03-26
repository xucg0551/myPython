from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from multiprocessing.managers import BaseManager
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
import time

class SpiderWork(object):
    def __init__(self):
        # 实现第一步：使用BaseManager注册获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 实现第二步：连接到服务器:
        print('Connect to server {}...'.format(settings.HOST))
        # 端口和验证口令注意保持与服务进程设置的完全一致:
        self.m = BaseManager(address=(settings.HOST, settings.PORT), authkey='baike'.encode())
        # 从网络连接:
        self.m.connect()
        # 实现第三步：获取Queue的对象:
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        # 初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        while(True):
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url =='end':
                        print('控制节点通知爬虫节点停止工作..')
                        #接着通知其它节点停止工作
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print('爬虫节点正在解析:%s'%url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls,data = self.parser.parser(url,content)
                    print('--------------------new_urls----------------:')
                    print(new_urls)
                    print('-------------------data--------------------')
                    print(data)
                    self.result.put({"new_urls":new_urls,"data":data})
                else:
                    print('task is empty now!!!')
                    time.sleep(1)
            except EOFError as e:
                print('连接工作节点失败')
                return
            except Exception as e:
                print(e)
                print('Crawl  fali')

if __name__=="__main__":
    spider = SpiderWork()
    spider.crawl()



