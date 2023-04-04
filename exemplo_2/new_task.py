"""
https://www.rabbitmq.com/tutorials/tutorial-two-python.html
#Objetivo desse exemplo é distribuir tarefas demoradas entre vários workers

A ideia principal por trás das Filas de Trabalho (também conhecidas como Filas de Tarefas )
é evitar fazer uma tarefa com uso intensivo de recursos imediatamente e ter que esperar que ela seja concluída. 
Em vez disso, agendamos a tarefa para ser realizada posteriormente. Encapsulamos uma tarefa como uma mensagem e a 
enviamos para a fila. Um processo de trabalho em execução em segundo plano exibirá as tarefas e, eventualmente, 
executará o trabalho. Quando você executar muitos workers, as tarefas serão compartilhadas entre eles.
"""
    
import pika, sys

#estabelece a conexao com rabbitmq - ip conteiner rabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters( '172.17.0.2' ))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

"""
Vai enviar uma string com pontos, onde cada ponto irá corresponder a 1 segundo de atraso na função callback do reciver.py
ao chamar o new_tak.py no terminal add uma mesnagem+pontos, onde cada ponto corresponde por um segundo de atraso para ver o exemplo funcionar
exemplo: $ python new_task.py MENSAGEM DE TESTE ...
"""

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE) #marcando as mensagens como persistente
    )
print(" [x] Sent %r" % message)
channel.close()