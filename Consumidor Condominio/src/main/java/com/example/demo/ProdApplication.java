package com.example.demo;

import org.springframework.amqp.core.TopicExchange;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class ProdApplication {

	static final String topicExchange = "topic-exchange";

	@Bean
	TopicExchange exchange() {
		return new TopicExchange(topicExchange, false, true);
	}

	public static void main(String[] args) {
		SpringApplication.run(ProdApplication.class, args);
	}
}
