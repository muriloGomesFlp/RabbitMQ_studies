#!/usr/bin/env python
import pika
import uuid

"""
Observação sobre RPC
Embora o RPC seja um padrão bastante comum na computação, ele é frequentemente criticado. 
Os problemas surgem quando um programador não sabe se uma chamada de função é local ou se é um RPC lento. 
Confusões como essa resultam em um sistema imprevisível e adicionam complexidade desnecessária à depuração. 
Em vez de simplificar o software, o RPC mal utilizado pode resultar em um código espaguete insustentável.

Tendo isso em mente, considere os seguintes conselhos:

Certifique-se de que é óbvio qual chamada de função é local e qual é remota.
Documente seu sistema. Deixe claras as dependências entre os componentes.
Tratar casos de erro. Como o cliente deve reagir quando o servidor RPC fica inativo por um longo período?

Em caso de dúvida, evite RPC. Se puder, você deve usar um pipeline assíncrono - em vez do bloqueio do tipo RPC, 
os resultados são enviados de forma assíncrona para um próximo estágio de computação.
"""

class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='172.17.0.2'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        """
        Propriedades da mensagem => pika.BasicProperties
        O protocolo AMQP 0-9-1 predefine um conjunto de 14 propriedades que acompanham uma mensagem. 
        A maioria das propriedades raramente é usada, com exceção do seguinte:

        delivery_mode : Marca uma mensagem como persistente (com valor 2 ) ou transiente (qualquer outro valor). 
        Você deve se lembrar dessa propriedade do segundo tutorial .
        content_type : Usado para descrever o tipo mime da codificação. Por exemplo, para a codificação JSON frequentemente usada, 
        é uma boa prática definir essa propriedade como: application/json .
        reply_to : Comumente usado para nomear uma fila de retorno de chamada.
        correlação_id : Útil para correlacionar respostas RPC com solicitações.
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                #reply_to=> metodo que irá receber a resposta (callback)
                reply_to=self.callback_queue,
                #correlation_id => diz a qual solicitação a resposta pertence
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

#Ele vai expor um método chamado call que envia uma requisição RPC e BLOQUEIA até que a resposta seja recebida
print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)