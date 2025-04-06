import pika
import ssl
import certifi
import logging

# Configura o logging para registrar em um arquivo "log.txt"
logging.basicConfig(
    filename='auditoria-log.txt',      # Nome do arquivo de log
    filemode='a',            # 'a' para acrescentar (append) a cada nova execução
    level=logging.INFO,      # Nível de log: INFO, DEBUG, etc.
    format='%(levelname)s - %(message)s'  # Formato da mensagem de log
)

def main():
    url = 'amqps://tskvjkbi:u9k0vaTKJOIlzmxIv6Zc9OdyaOH8h52L@hawk-01.rmq.cloudamqp.com/tskvjkbi'
    params = pika.URLParameters(url)

    # Configurar SSL com certifi
    context = ssl.create_default_context(cafile=certifi.where())
    params.ssl_options = pika.SSLOptions(context)

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    topic_exchange = "topic-exchange"
    queue_name = "auditoria-queue"

    # Declara o exchange tipo topic
    channel.exchange_declare(
        exchange=topic_exchange,
        exchange_type="topic",
        durable=False,
        auto_delete=True
    )

    # Declara a fila de auditoria
    channel.queue_declare(queue=queue_name)

    # Faz o binding com '#' para receber todas as mensagens
    channel.queue_bind(
        exchange=topic_exchange,
        queue=queue_name,
        routing_key="#"
    )

    # Registra no log que o auditor foi iniciado
    logging.info("Auditoria iniciada. Conectado à CloudAMQP, aguardando mensagens...")
    print("[Auditoria] Recebendo TODAS as mensagens...")

    def callback(ch, method, properties, body):
        routing_key = method.routing_key
        mensagem = body.decode()
        log_msg = f"[AUDITORIA] -> Rota '{routing_key}': {mensagem}"
        print(log_msg)
        logging.info(log_msg)  # Registra a mensagem recebida no log

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    main()