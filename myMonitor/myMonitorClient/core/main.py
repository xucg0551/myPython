#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-


from . import client

class CommandHandler(object):
    def __init__(self, sys_args):
        self.sys_args = sys_args
        #如果启动没有带参数，退出并提示
        if len(sys_args) < 2 :
            self.exit_message()
        self.allocator()

    #根据输入的参数进行反射，
    def allocator(self):
        if hasattr(self, self.sys_args[1]):
            func = getattr(self, self.sys_args[1])
            func()
        else:
            print('command does not exist')
            self.exit_message()


    #启动服务
    def start(self):
        a_client = client.ClientHandler()
        a_client.run_forever()


    def end(self):
        pass

    #程序退出
    def exit_message(self):
        message = '''
        start   start monitor clinet
        stop    stop monitor client
        '''
        exit(message)

