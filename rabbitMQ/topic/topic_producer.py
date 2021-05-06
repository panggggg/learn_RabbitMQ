import pika
import json
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="order.topic", exchange_type="topic")


order = {
    "id": str(uuid.uuid4()),
    "user_email": "p.picczy@gmail.com",
    "product": "Jelly",
    "quantity": 1,
}

channel.basic_publish(
    exchange="order.topic",
    routing_key="test.any",
    body=json.dumps({"product": order["product"]}),
)

print("[x] Sent information message")

connection.close()
