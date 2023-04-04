import pika

#estabelece a conexao com rabbitmq - ip conteiner rabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters( '172.17.0.2' ))
channel = connection.channel()

#criando a fila no RabbitMQ
#queue_declare é idempotente ‒ podemos executar o comando quantas vezes quisermos e apenas uma será criada.
channel.queue_declare(queue='hello')

#enviando a menssagem para fila
channel.basic_publish(
    exchange= '' , #tuto 3=> publish/subscribe
    routing_key = 'hello' ,# => diz para qual fila será enviado
    body= 'Olá mundo!' # => Conteudo da menssagem
    )

#fecha a conexão
channel.close()
print( "[x] Enviado 'Hello World!'" )