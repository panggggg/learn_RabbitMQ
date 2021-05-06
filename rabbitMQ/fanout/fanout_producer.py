import pika
import json
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="order.fanout", exchange_type="fanout")


order = {
    "id": str(uuid.uuid4()),
    "user_email": "p.picczy@gmail.com",
    "product": "Jelly",
    "quantity": 1,
}

channel.basic_publish(exchange="order.fanout", routing_key="", body=json.dumps(order))
print("[x] Sent information message")

connection.close()