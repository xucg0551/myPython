#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import pika

queue_name = 'queue_demo.com'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#声明queqe, 且queue名持久化
channel.queue_declare(queue=queue_name, durable=True)

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body='Hello World!',
                      properties=pika.BasicProperties(
                          delivery_mode=2  #消息持久化
                      ))

print(' [x] Sent "Hello World!"')
connection.close()

