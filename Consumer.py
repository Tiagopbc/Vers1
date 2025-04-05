import pika
import ssl
import certifi


def main():
    url = 'amqps://tskvjkbi:u9k0vaTKJOIlzmxIv6Zc9OdyaOH8h52L@hawk-01.rmq.cloudamqp.com/tskvjkbi'
    params = pika.URLParameters(url)

    # Cria um contexto SSL apontando pro cacert.pem do certifi
    context = ssl.create_default_context(cafile=certifi.where())
    params.ssl_options = pika.SSLOptions(context)

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    topic_exchange = 'topic-exchange'

    # Declara o exchange tipo topic
    channel.exchange_declare(
        exchange=topic_exchange,
        exchange_type='topic',
        durable=False,
        auto_delete=True
    )

    # Cria uma fila exclusiva com nome random
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    print("\n=== Consumidor ===")
    print("Escolha em quais blocos deseja se inscrever.")
    print("Exemplos:")
    print("- Digite 'A' para Bloco A")
    print("- Digite 'A,B' para Bloco A e Bloco B")
    print("- Digite 'TODOS' para receber de todos os blocos\n")

    opcao = input("Digite sua escolha: ").strip().upper()

    # Se o usuário digitar "TODOS", faz binding com '#' (significa todas as rotas)
    if opcao == "TODOS":
        binding_keys = ["bloco.#"]
    else:
        # Exemplo: se o usuário digitar "A,B,E", vamos gerar:
        #   bloco.A.#
        #   bloco.B.#
        #   bloco.E.#
        # Assim ele recebe avisos de todos esses blocos
        blocos = [b.strip() for b in opcao.split(',')]
        binding_keys = [f"bloco.{bloco}.#" for bloco in blocos]

        # Agora, adicionamos também 'bloco.geral.aviso' (ou 'bloco.geral.#')
        # para receber as mensagens de "TODOS" que o produtor manda (ex: "bloco.geral.aviso").
        # Isso garante que mesmo quem escolheu A,C também receba as mensagens gerais.
        binding_keys.append("bloco.geral.#")

    # Faz o binding da fila com cada binding_key selecionada
    for bk in binding_keys:
        channel.queue_bind(
            exchange=topic_exchange,
            queue=queue_name,
            routing_key=bk
        )
        print(f"[✓] Inscrito na routing key '{bk}'")

    print("\n[✓] Conectado à CloudAMQP! Aguardando mensagens...\n")

    def callback(ch, method, properties, body):
        print(f"[→] Mensagem recebida: {body.decode()} (routing_key={method.routing_key})")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()


if __name__ == "__main__":
    main()
