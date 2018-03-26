import pickle
import hashlib

class UrlManager(object):
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt')  # 未爬取URL集合
        self.old_urls = self.load_progress('old_urls.txt')  # 已爬取URL集合

    def has_new_url(self):
        '''
        判断是否有未爬取的URL
        :return:
        '''
        return self.new_url_size() != 0

    def get_new_url(self):
        '''
        获取一个未爬虫的url，且把其md5后加入已爬虫的url中
        :return:
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(self.get_md5(new_url))
        return new_url

    def add_new_url(self, url):
        '''
        将新的url添加到未爬取的url集合中
        :param url: 待添加的url
        :return:
        '''
        if url is None:
            return
        url_md5 = self.get_md5(url)
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        将新的urls添加到未爬取的url集合中
        :param urls:
        :return:
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        '''
        获取未爬取url集合的大小
        :return:
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''
        获取已经爬取url集合的大小
        :return:
        '''
        return len(self.old_urls)

    def save_progress(self, path, data):
        '''
        保存爬取进度
        :param path: 文件路径
        :param data: 数据
        :return:
        '''
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        '''
        加载爬取进度
        :param path:
        :return:
        '''
        print('[+] 从文件加载进度: {}'.format(path))
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except:
                print('[!] 无进度文件, 创建: {}'.format(path))
        return set()

    def get_md5(self, text):
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()[8:-8]  #取md5的16位