#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import configparser

#写操作
config = configparser.ConfigParser()
config["DEFAULT"] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                     'CompressionLevel': '9'}

config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'

config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Host Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'


#读操作
with open('config.ini', 'w') as configfile:
    config.write(configfile)

#读操作
config = configparser.ConfigParser()
config.read('config.ini')
print('bitbucket.org' in config)
print(config['DEFAULT']['ServerAliveInterval'])
for key in config['DEFAULT']:
    print(config['DEFAULT'][key])

