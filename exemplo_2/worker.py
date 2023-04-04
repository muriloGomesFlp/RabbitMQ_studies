# importa a instanciação da conexão
import pika, sys, os
from time import sleep
"""
O rabbitMQ envia a msg para o próximo consumidor em sequencia, sendo que em média cada consumidor irá receber o mesmo número de menssagem. 
Essa maneira de distribuir as mensagens é chamada de round-robin.
"""


def main():
    #estabelece a conexao com rabbitmq - ip conteiner rabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters( '172.17.0.2' ))
    channel = connection.channel()

    """queue_declare é idempotente ‒ podemos executar o comando quantas vezes quisermos e apenas uma será criada.
    boa prática sempre criar a fila, pois não sabe a ordem ou qual programa irá executar primeiro
    O 
    """
    channel.queue_declare(queue='task_queue', durable=True)
    print( ' [*] Aguardando mensagens. Para sair aperte CTRL+C' ) 



    '''
    Receber mensagens da fila é mais complexo. Ele funciona inscrevendo uma função de retorno (callback) de chamada em uma fila. 
    Sempre que recebemos uma mensagem, essa função de callback é chamada pela biblioteca Pika.
    Nesse caso esta função imprimirá na tela o conteúdo da mensagem.
    '''

    def callback(ch, method, properties, body):
        print("[x] Received %r" % body.decode())
        time = body.count( b'.' )
        sleep(time) 
        print(f'[x] Done - wait {time}')
        """Garante que a mensagem não será perdida caso o worker morra (confirmação de mensagem), 
        sendo enviada pelo consumidor ao RabbitMQ que a mensagem foi recebida,processada e pode ser excluida da fila. 
        OBS.: Um tempo limite (30 minutos por padrão) é aplicado na confirmação de entrega do consumidor, mas pode ser alterado."""
        ch.basic_ack(delivery_tag=method.delivery_tag)
        """
        https://www.rabbitmq.com/confirms.html
        basic.ack é usado para confirmações positivas 
        basic.nack é usado para confirmações negativas 
        basic.reject é usado para confirmações negativas, mas tem uma limitação em comparação com basic.nack
        """

    """channel.basic_qos => diz ao RabbitMQ para não enviar mais de uma mensagem para um trabalhador por vez. 
    Ou, em outras palavras, não despache uma nova mensagem para um worker até que ele tenha processado e reconhecido a anterior. """
    channel.basic_qos(prefetch_count=1)
    # diz ao rebbitMQ qual função irá receber a menssagem da fila "hello"
    channel.basic_consume(
        # foi removido o auto_ack para poder garantir que a mensagem não se perca mesmo se o worker morrer. Foi definifo na func callback linha 32
        queue='task_queue', # => Nome da fila que possui a menssagem
        on_message_callback=callback # => Função que irá receber a menssagem
        )
        

    # incia um loop em fim para recebimento de mensagens
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