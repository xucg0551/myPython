import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel() #声明一个管道

channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct'
)
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write('Usage:{} [info] [warning] [error]\n'.format(sys.argv[0]))
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange='direct_logs',
        queue=queue_name,
        routing_key=severity
    )

print('[*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print('[x] Received {}'.format(body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()