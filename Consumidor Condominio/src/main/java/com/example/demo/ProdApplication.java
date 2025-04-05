package com.example.demo;

import org.springframework.amqp.core.TopicExchange;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class ProdApplication {

	// Em vez de "direct-exchange"
	static final String topicExchangeName = "topic-exchange"; // nome que preferir

	@Bean
	TopicExchange exchange() {
		// autoDelete = true (conforme seu exemplo), durable = false
		return new TopicExchange(topicExchangeName, false, true);
	}

	public static void main(String[] args) {
		SpringApplication.run(ProdApplication.class, args);
	}
}
