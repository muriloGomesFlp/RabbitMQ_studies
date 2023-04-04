#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()
    """
    a comunicação entre produtor de as filas não são mais diretas, utilizando uma exchange (troca).
    A ideia central no modelo de mensagens no RabbitMQ é que o produtor nunca envie nenhuma mensagem diretamente para uma fila.
    Existem alguns tipos de troca disponíveis: direct , topic , headers e fanout (espalha para as filas)
"""
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    #sempre que conectar ao Rabbit, uma fila nova e vazia. 
    # Além disso o uso do exclusive permite ao encerrar a conexão do consumidor a fila seja excluída.
    result = channel.queue_declare(queue='', exclusive=True)
    #e será gerada com um novo nome aleatório
    queue_name = result.method.queue

    #diz ao exchange para qual fila deve enviar
    channel.queue_bind(exchange='logs', queue=queue_name)

    def callback(ch, method, properties, body):
        print(" [x] %r" % body.decode())

    print(' [*] Waiting for logs. To exit press CTRL+C')
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