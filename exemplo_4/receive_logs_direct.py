#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    #O significado de uma routing_key (é diferente do routing_key do método basic_publish) depende do tipo de troca. 
    # As trocas fanout , que usamos anteriormente, simplesmente ignoraram seu valor.
    for severity in severities:
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body.decode()))


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)