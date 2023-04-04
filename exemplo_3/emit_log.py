#https://www.rabbitmq.com/tutorials/tutorial-three-python.html
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

"""
a comunicação entre produtor de as filas não são mais diretas, utilizando uma exchange (troca).
A ideia central no modelo de mensagens no RabbitMQ é que o produtor nunca envie nenhuma mensagem diretamente para uma fila.
Existem alguns tipos de troca disponíveis: direct , topic , headers e fanout (espalha para as filas)
"""
channel.exchange_declare(exchange='logs', exchange_type='fanout')

"""
com exchange declarado, não é necessário informar o nome da fila, pois agora as filas serão criadas atumaticamente pelo RabbitMQ
Assim o RabbitMQ irá "ouvir" todas as menssagens do tipo 'logs", não apenas um subconjunto delas.
"""
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()