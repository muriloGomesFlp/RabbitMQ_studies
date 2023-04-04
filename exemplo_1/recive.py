# importa a instanciação da conexão
import pika, sys, os

def main():
    #estabelece a conexao com rabbitmq - ip conteiner rabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters( '172.17.0.2' ))
    channel = connection.channel()

    #queue_declare é idempotente ‒ podemos executar o comando quantas vezes quisermos e apenas uma será criada.
    # boa prática sempre criar a fila, pois não sabe a ordem ou qual programa irá executar primeiro
    channel.queue_declare(queue= 'hello' )

    '''
    Receber mensagens da fila é mais complexo. Ele funciona inscrevendo uma função de retorno (callback) de chamada em uma fila. 
    Sempre que recebemos uma mensagem, essa função de callback é chamada pela biblioteca Pika.
    Nesse caso esta função imprimirá na tela o conteúdo da mensagem.
    '''

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())

    # diz ao rebbitMQ qual função irá receber a menssagem da fila "hello"
    channel.basic_consume(
        queue='hello', # => Nome da fila que possui a menssagem
        auto_ack=True, # Entendimento no exemplo 2 - Work queue
        on_message_callback=callback # => Função que irá receber a menssagem
        )

    # incia um loop em fim para recebimento de menssagens
    print( ' [*] Aguardando mensagens. Para sair aperte CTRL+C' ) 
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