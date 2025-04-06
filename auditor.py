import pika
import ssl
import certifi

url = 'amqps://tskvjkbi:u9k0vaTKJOIlzmxIv6Zc9OdyaOH8h52L@hawk-01.rmq.cloudamqp.com/tskvjkbi'
params = pika.URLParameters(url)

# Configurar SSL com certifi
context = ssl.create_default_context(cafile=certifi.where())
params.ssl_options = pika.SSLOptions(context)

# Cria a conexão e um canal
connection = pika.BlockingConnection(params)
channel = connection.channel()

exchange_name = "topic-exchange"
queue_name = "auditoria-queue"

# Declara o exchange do tipo topic (se já existir, não faz mal)
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type="topic",
    durable=False,
    auto_delete=True
)

# Declara a fila da auditoria
channel.queue_declare(queue=queue_name)

# Faz bind com '#' para receber todas as mensagens enviadas para o exchange
channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key="#"
)

print("[Auditoria] Recebendo TODAS as mensagens...")


def callback(ch, method, properties, body):
    # Recupera a routing key (bloco ou rota)
    routing_key = method.routing_key
    # Decodifica o corpo da mensagem
    mensagem = body.decode()

    print(f"[AUDITORIA] -> Rota '{routing_key}': {mensagem}")


# Consumindo da fila auditoria-queue
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

# Inicia o loop de consumo
channel.start_consuming()
