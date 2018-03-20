#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import pika

queue_name = 'queue_demo.com'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'
))
channel = connection.channel()

channel.queue_declare(queue=queue_name, durable=True)

def callback(ch, method, properties, body):
    print('[x] Received {}'.format(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback, queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()