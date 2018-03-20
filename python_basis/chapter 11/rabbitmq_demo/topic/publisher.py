import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel() #声明一个管道

channel.exchange_declare(exchange = 'topic_logs',
                         exchange_type = 'topic')

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(
    exchange='topic_logs',
    routing_key=routing_key,
    body=message,
)

print('[x] Sent {} {}'.format(routing_key, message))
connection.close()