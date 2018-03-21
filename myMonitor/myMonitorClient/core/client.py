#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
from urllib import request
import time
from config import settings
import json
from urllib import error


class ClientHandler(object):
    def __init__(self):
        self.monitored_services = {}

    #向服务器请求最新配置信息
    def request_latest_configs(self):
        request_type = settings.configs['urls']['get_configs'][1]
        request_url = '{}/{}'.format(settings.configs['urls']['get_configs'][0], settings.configs['HostID'])
        data = self.request_data(request_type, request_url)
        latest_configs = json.loads(data)
        print(latest_configs)

    #请求数据
    def request_data(self, action, url, **datas):
        http_url = 'http://{}:{}/{}'.format(settings.configs['Server'], settings.configs['ServerPort'], url)
        if action in ('get', 'GET'): #get请求
            req = request.Request(http_url)
            try:
                data = request.urlopen(req, timeout=settings.configs['RequestTimeout']).read().decode('utf8')
                return data
            except error.URLError as e:  #判断异常  HTTPError是URLError, HTTPError有code属性
                if hasattr(e, 'code'):
                    print(e.code)
                if hasattr(e, 'reason'):
                    print(e.reason)
                exit("\033[31;1m%s\033[0m" % e)
        elif action in ('post', 'POST'):  #post请求
            pass


    #执行操作
    def run_forever(self):
        exit_flag = False
        config_last_update_time = 0
        while not exit_flag:
            #当超过更新间隙，则向服务器请求更新数据
            if time.time() - config_last_update_time > settings.configs['ConfigUpdateInterval']:
                print('"Loaded latest config:", self.monitored_services')
                self.request_latest_configs()
                config_last_update_time = time.time()

