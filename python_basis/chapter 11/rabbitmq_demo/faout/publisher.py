#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel() #声明一个管道

channel.exchange_declare(exchange = 'logs',exchange_type = 'fanout')

message = 'info: Hello World!'
channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message,
)

print('[x] Sent "Hello World!"')
connection.close()