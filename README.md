# 🏢 Central de Notificações do Prédio

Este projeto simula uma central de notificações para um condomínio, utilizando comunicação assíncrona via **RabbitMQ (AMQP)** entre serviços desenvolvidos em **Java (Spring Boot)** e **Python**.

## 📌 Descrição

O sistema é composto por três partes:

- ✅ **Produtor (Java/Spring Boot)**: envia avisos para diferentes blocos do prédio.
- 📬 **Consumidor (Python)**: se inscreve em blocos específicos e recebe notificações.
- 📜 **Auditor (Python)**: escuta todas as mensagens e salva um log.


## 🔧 Tecnologias

- Java 17 (Spring Boot)
- Python 3.10+
- RabbitMQ (CloudAMQP)
- Pika + Certifi (Python)

## 🧠 Conceitos

- **AMQP**: protocolo de mensagens assíncronas.
- **Topic Exchange**: roteamento baseado em padrões como `bloco.A.#`.
- **SSL/Certifi**: conexão segura com o broker AMQP.

## 📂 Estrutura

java/: ProdApplication.java, Runner.java python/: Consumer.py, auditor.py

shell
Copy
Edit

## ▶️ Execução

### 1. Instalar dependências (Python)

```bash
pip install pika certifi
```

### 2. Rodar o produtor (Java)

```bash
./mvnw spring-boot:run
3. Rodar os consumidores (Python)
```

```
bash
python Consumer.py     # Consumidor por bloco
python auditor.py      # Auditor
```
