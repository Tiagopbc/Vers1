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

    while True:
        print("\n" + "=" * 50)
        print("     🏢  CENTRAL DE NOTIFICAÇÃO DO PRÉDIO")
        print("=" * 50 + "\n")

        print("📍 Escolha em quais blocos deseja se inscrever:")
        print("   ➤ Digite 'A' para Bloco A")
        print("   ➤ Digite 'A,B' para Bloco A e Bloco B")
        print("   ➤ Digite 'TODOS' para receber de todos os blocos\n")

        opcao = input("🔸 Sua escolha: ").strip().upper()

        if opcao == "TODOS" or opcao == "todos" or opcao == "A,B,C,D,E":
            binding_keys = ["bloco.#"]
        elif opcao in [
            "A", "B", "C", "D", "E",
            "A,B", "A,C", "A,D", "A,E",
            "B,C", "B,D", "B,E",
            "C,D", "C,E", "D,E",
            "A,B,C", "A,B,D", "A,B,E",
            "A,C,D", "A,C,E", "A,D,E",
            "B,C,D", "B,C,E", "B,D,E",
            "C,D,E", "A,B,C,D", "A,B,C,E",
            "A,B,D,E", "A,C,D,E", "B,C,D,E",
        ]:
            blocos = [b.strip() for b in opcao.split(',')]
            binding_keys = [f"bloco.{bloco}.#" for bloco in blocos]
        else:
            print("\n[✗] Opção inválida! Tente novamente.")
            print("[!] Exemplos válidos: 'A', 'B,C', ou 'TODOS'\n")
            continue

        print("\n📡 Inscrevendo nos blocos selecionados...\n")
        for bk in binding_keys:
            channel.queue_bind(
                exchange=topic_exchange,
                queue=queue_name,
                routing_key=bk
            )
            if bk == "bloco.#":
                print("  ✅ Inscrito em: 'TODOS os blocos'")
            else:
                print(f"  ✅ Inscrito em: '{bk}'")

        print("\n🔗 Conectado à CloudAMQP! Aguardando mensagens...\n")

        def callback(ch, method, properties, body):
            print(f"📬 Nova mensagem: '{body.decode()}'  Chave de Roteamento: ({method.routing_key})")

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        channel.start_consuming()

if __name__ == "__main__":
    main()
