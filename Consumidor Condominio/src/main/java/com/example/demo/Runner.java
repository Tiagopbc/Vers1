package com.example.demo;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.stereotype.Component;

@Component
public class Runner implements CommandLineRunner {

    private final RabbitTemplate rabbitTemplate;
    private final ConfigurableApplicationContext context;

    // Construtor
    public Runner(RabbitTemplate rabbitTemplate, ConfigurableApplicationContext context) {
        this.rabbitTemplate = rabbitTemplate;
        this.context = context;
    }

    @Override
    public void run(String... args) {
        Scanner scan = new Scanner(System.in);

        // Cabeçalho inicial
        System.out.println("\n==================================================");
        System.out.println("           PRODUTOR DE AVISOS (JAVA)");
        System.out.println("==================================================");
        System.out.println("Pressione ENTER para iniciar ou digite 'sair' a qualquer momento para encerrar...\n");

        while (true) {
            // Solicita qual bloco o usuário deseja enviar a mensagem
            System.out.println("Para qual bloco deseja enviar o aviso? (A, B, C, D, E ou 'TODOS')");
            String bloco = scan.nextLine().trim();
            if (bloco.equalsIgnoreCase("sair")) break;

            // Define a routing key de acordo com a escolha
            String routingKey;
            switch (bloco.toUpperCase()) {
                case "A": routingKey = "bloco.A.aviso"; break;
                case "B": routingKey = "bloco.B.aviso"; break;
                case "C": routingKey = "bloco.C.aviso"; break;
                case "D": routingKey = "bloco.D.aviso"; break;
                case "E": routingKey = "bloco.E.aviso"; break;
                case "TODOS":
                    // Envia para todos os blocos (padrão: bloco.geral.aviso)
                    routingKey = "bloco.geral.aviso";
                    break;
                default:
                    System.out.println("Opção inválida. Tente novamente.\n");
                    continue;
            }

            // Solicita a mensagem que será enviada
            System.out.println("Digite a mensagem para o Bloco " + bloco + " (ou 'sair' p/ encerrar):");
            String msg = scan.nextLine();
            if (msg.equalsIgnoreCase("sair")) break;

            // Formata a mensagem com data/hora e remetente
            String dataHora = new SimpleDateFormat("dd/MM/yyyy - HH:mm:ss").format(new Date());
            String nomeProdutor = "Administrador do Condomínio";
            String mensagemFinal = String.format("[%s] %s : %s", dataHora, nomeProdutor, msg);

            // Envia a mensagem para o RabbitMQ
            rabbitTemplate.convertAndSend(
                ProdApplication.topicExchange, // Nome do exchange
                routingKey,
                mensagemFinal
            );

            // Confirmação de envio
            System.out.println("\n--------------------------------------------------");
            System.out.println("Mensagem enviada com sucesso!");
            System.out.println("Exchange   : " + ProdApplication.topicExchange);
            System.out.println("Routing Key: " + routingKey);
            System.out.println("Mensagem   : " + mensagemFinal);
            System.out.println("--------------------------------------------------\n");
        }

        // Encerra a aplicação com segurança
        System.out.println("\nEncerrando aplicação Java (Produtor). Até a próxima!");
        context.close();
    }
}
