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

        System.out.println("=== PRODUTOR DE AVISOS (Java) ===");
        System.out.println("Pressione ENTER para iniciar ou digite 'sair' a qualquer momento para encerrar...");

        while(true) {
            System.out.println("\nPara qual bloco deseja enviar o aviso? (A, B, C, D, E ou 'todos')");
            String bloco = scan.nextLine().trim();
            if(bloco.equalsIgnoreCase("sair")) break;

            // Definir a routing key de acordo com a escolha do bloco
            String routingKey;
            switch(bloco.toUpperCase()) {
                case "A": routingKey = "bloco.A.aviso"; break;
                case "B": routingKey = "bloco.B.aviso"; break;
                case "C": routingKey = "bloco.C.aviso"; break;
                case "D": routingKey = "bloco.D.aviso"; break;
                case "E": routingKey = "bloco.E.aviso"; break;
                case "TODOS":
                    // Exemplo: 'todos.aviso' ou mesmo 'bloco.#'
                    // Mas normalmente, para mandar para todos, é legal padronizar
                    // algo como 'bloco.geral.aviso' e os consumidores usam `bloco.#`
                    routingKey = "bloco.geral.aviso";
                    break;
                default:
                    System.out.println("Opção inválida. Tente novamente.");
                    continue;
            }

            System.out.println("Digite a mensagem para o Bloco "+bloco+" (ou 'sair' p/ encerrar):");
            String msg = scan.nextLine();
            if(msg.equalsIgnoreCase("sair")) break;

            // Montar o formato exigido: [dd/MM/yyyy - HH:mm] Produtor : corpo_da_mensagem
            String dataHora = new SimpleDateFormat("dd/MM/yyyy - HH:mm:ss").format(new Date());
            String nomeProdutor = "Administrador do Condomínio"; // Ajuste como quiser
            String mensagemFinal = String.format("[%s] %s : %s", dataHora, nomeProdutor, msg);

            // Envia a mensagem
            rabbitTemplate.convertAndSend(
                    ProdApplication.topicExchangeName, // "topic-exchange"
                    routingKey,
                    mensagemFinal
            );

            System.out.println("Mensagem enviada -> exchange: " + ProdApplication.topicExchangeName +
                    " | routingKey: " + routingKey +
                    " | msg: " + mensagemFinal);
        }

        System.out.println("\nEncerrando aplicação Java (Produtor)...");
        context.close();
    }
}
