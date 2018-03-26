from multiprocessing.managers import BaseManager
from multiprocessing import Queue, Process
from UrlManager import UrlManager
from DataOutput import DataOutput
import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

class NodeManager(object):
    def start_manager(self, url_queue, result_queue):
        '''
        创建一个分布式管理器
        :param url_queue:
        :param result_queue:
        :return:
        '''
        # 把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，
        # 将Queue对象在网络中暴露
        BaseManager.register('get_task_queue', callable=lambda :url_queue)
        BaseManager.register('get_result_queue', callable=lambda : result_queue)
        # 设置host, 绑定端口，设置验证口令‘baike’。这个相当于对象的初始化
        manager = BaseManager(address=(settings.HOST, settings.PORT), authkey='baike'.encode())
        return manager

    def url_manage_process(self, url_queue, connect_queue, root_url):
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            #先while循环访问set里的url，如果没有新的url则从connect_queue中获取再放到set中
            while url_manager.has_new_url():
                #从url管理器获取新的url
                new_url = url_manager.get_new_url()
                #将新的url分发给工作节点
                url_queue.put(new_url)
                print('old_url=', url_manager.old_url_size())
                #当爬取2000个链接后就关闭，并保存进度
                if url_manager.old_url_size() > settings.VISITED_MAX:
                    #通知爬取节点结束
                    url_queue.put('end')
                    print('控制节点发起结束通知')
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)
                    return
            #从connect_queue(result_solve_process处理)获取urls
            try:
                if not connect_queue.empty():
                    urls = connect_queue.get()
                    url_manager.add_new_urls(urls)
            except Exception as e:
                print(e)
                time.sleep(0.1)

    def result_manage_process(self, result_queue, connect_queue, store_queue):
        while True:
            try:
                if not result_queue.empty():
                    content = result_queue.get(True)
                    if content['new_urls'] == 'end':
                        print('结果分析进程接受通知然后结束')
                        store_queue.put('end')
                        return

                    connect_queue.put(content['new_urls'])
                    store_queue.put(content['data'])
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(e)
                time.sleep(0.1)

    def store_process(self, store_queue):
        output = DataOutput()
        while True:
            if not store_queue.empty():
                data = store_queue.get()
                if data == 'end':
                    print('存储进程接受通知然后结束!')
                    output.ouput_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)





if __name__ == '__main__':
    #初始化4个队列
    url_queue = Queue()
    result_queue = Queue()
    store_queue = Queue()
    connect_queue = Queue()

    #创建分布式管理器
    node = NodeManager()
    manager = node.start_manager(url_queue, result_queue)

    # 创建URL管理进程、 数据提取进程和数据存储进程
    url_manager_process = Process(target=node.url_manage_process, args=(url_queue, connect_queue, 'http://baike.baidu.com/view/284853.htm',))
    result_manage_process = Process(target=node.result_manage_process, args=(result_queue, connect_queue, store_queue,))
    store_process = Process(target=node.store_process, args=(store_queue,))

    # 启动3个进程和分布式管理器
    url_manager_process.start()
    result_manage_process.start()
    store_process.start()
    manager.get_server().serve_forever()
