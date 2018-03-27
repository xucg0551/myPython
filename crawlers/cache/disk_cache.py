#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import urllib.parse
import re, os
import pickle
import zlib
import shutil
from link_crawler import link_crawler

class DiskCache:

    def __init__(self, cache_dir='cache', expires=timedelta(days=30), compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress


    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result

        else:
            raise KeyError(url + ' dose not exist')


    def __setitem__(self, url, result):

        #等判断文件夹是否存在，再判断是否要压缩，最后把数据序列化放到文件中
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __delitem__(self, url):
        path = self.url_to_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            path



    def has_expired(self, timestamp):
        return datetime.utcnow() > (timestamp + self.expires)

    def clear(self):
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)



    def url_to_path(self, url):
        """Create file system path for this URL
                """
        components = urllib.parse.urlsplit(url)
        # when empty path set to /index.html
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        print(filename)
        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '+', filename)
        # restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)



if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', cache=DiskCache())

