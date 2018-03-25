import requests
from faker import Factory
f = Factory.create()
USER_AGENT = f.user_agent()

class HtmlDownloader(object):

    def download(self,url):
        if url is None:
            return None
        headers={'User-Agent':USER_AGENT}
        r = requests.get(url,headers = headers)
        if r.status_code==200:
            r.encoding='utf-8'
            return r.text
        return None
