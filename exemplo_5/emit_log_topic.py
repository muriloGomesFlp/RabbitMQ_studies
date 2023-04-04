#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()
"""
a comunicação entre produtor de as filas não são mais diretas, utilizando uma exchange (troca).
A ideia central no modelo de mensagens no RabbitMQ é que o produtor nunca envie nenhuma mensagem diretamente para uma fila.
Existem alguns tipos de troca disponíveis: 
* direct: direciona para a fila conforme a chave definida (funciona como um rotiamento) , 
* topic: uma maneira de direcionar as mensagen(roteamento), mas com maior flexibilidade. Para isso não tem uma chave arbitrária 
- deve ser uma lista de palavras delimitadas por pontos que especificam algumas características ligadas à mensagem. ex.:
anonymous.info, system.error, userX.info, etc. o tamanho da chave máxio é de 255bytes.
Pode haver ainda uso de caracteres para servir como "coringa", sendo(* substitu exatamente um palavra e # zero ou mais palavras). Caso 
o topico enviado não se encaixe em nenhuma regra será perdidos "ignorados".
* headers:
* fanout: espalha para as filas
"""
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()