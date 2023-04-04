#https://www.rabbitmq.com/tutorials/tutorial-four-python.html
import pika
import sys
"""
Neste tutorial vamos adicionar um recurso a ele - vamos possibilitar a assinatura apenas de um subconjunto das mensagens. 
Por exemplo, poderemos direcionar apenas mensagens de erro críticas para o arquivo de log (para economizar espaço em disco), 
enquanto ainda podemos imprimir todas as mensagens de log no console.
"""
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()
"""
a comunicação entre produtor de as filas não são mais diretas, utilizando uma exchange (troca).
A ideia central no modelo de mensagens no RabbitMQ é que o produtor nunca envie nenhuma mensagem diretamente para uma fila.
Existem alguns tipos de troca disponíveis: 
* direct: direciona para a fila conforme a chave definida (funciona como um rotiamento) , 
* topic: , 
* headers:
* fanout: espalha para as filas
"""
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()