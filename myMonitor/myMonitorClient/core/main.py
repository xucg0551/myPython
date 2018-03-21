#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
from . import client

class CommandLineHandler(object):
    def __init__(self, sys_args):
        #如果启动没有带参数，退出并提示
        self.help() if len(sys_args) < 2 else self.allocate(sys_args[1])

    #根据输入的命令行参数进行反射执行
    def allocate(self, func_str):
        getattr(self, func_str)() if hasattr(self, func_str) else self.help()

    #启动服务
    def start(self):
        client.ClientHandler().run_forever()

    #停止服务
    def end(self):
        pass

    #程序退出
    def help(self):
        message = '''
        start   start monitor clinet    eg. python  xxx.py  start
        stop    stop monitor client     eg. python  xxx.py  stop
        '''
        exit(message)

