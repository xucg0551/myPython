#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
from urllib import request, parse
import time
from config import settings
import json
from urllib import error
import threading
from plugins import plugin_api


class ClientHandler(object):
    def __init__(self):
        self.monitored_services = {}

    #向服务器请求最新配置信息
    def request_latest_configs(self):
        request_type = settings.configs['urls']['get_configs'][1]
        request_url = '{}/{}'.format(settings.configs['urls']['get_configs'][0], settings.configs['HostID'])
        data = self.request_data(request_type, request_url)
        latest_configs = json.loads(data)
        self.monitored_services.update(latest_configs)

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
            try:
                data_encode = parse.urlencode(datas['params'])
                req = request.Request(url=http_url,data=data_encode)
                res_data = request.urlopen(req,timeout=settings.configs['RequestTimeout'])
                callback = res_data.read()
                callback = json.loads(callback)
                print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" %(action,http_url,callback))
                return callback
            except Exception as e:
                print('---exec',e)
                exit("\033[31;1m%s\033[0m"%e)


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

            for service_name, val in self.monitored_services['services'].items():
                if len(val) == 2:  # means it's the first time to monitor
                    self.monitored_services['services'][service_name].append(0)
                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time > monitor_interval:
                    print(last_invoke_time, time.time())
                    self.monitored_services['services'][service_name][2] = time.time()
                    t = threading.Thread(target=self.invoke_plugin, args=(service_name,val))
                    t.start()
                    print("Going to monitor [%s]" % service_name)

    def invoke_plugin(self, service_name, val):
        plugin_name = val[0]
        if hasattr(plugin_api, plugin_name):
            print('plugin_api has {}'.format(plugin_name))
            func = getattr(plugin_api, plugin_name)
            plugin_callback = func()

            report_data = {
                'client_id': settings.configs['HostID'],
                'service_name': service_name,
                'data': json.dumps(plugin_callback)
            }

            request_action = settings.configs['urls']['service_report'][1]
            request_url = settings.configs['urls']['service_report'][0]
            print('---report data:', report_data)
            self.request_data(request_action, request_url, params=report_data)

        else:
             print("\033[31;1mCannot find service [%s]'s plugin name [%s] in plugin_api\033[0m"% (service_name,plugin_name ))
        print('--plugin:',val)



