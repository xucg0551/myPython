#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel() #声明一个管道

channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print('[*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print('[x] Received {}'.format(body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()