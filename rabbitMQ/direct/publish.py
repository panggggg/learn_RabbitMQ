import pika
import json
import uuid

# This file is Producer

# connect rabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# ประกาศชนิดของ exchange
channel.exchange_declare(exchange="order", exchange_type="direct")

channel.queue_bind(
    exchange="order", queue="order_notify", routing_key="order.notify"
)  # binding key

channel.queue_bind(exchange="order", queue="order_report", routing_key="order.report")

# ข้อมูล
order = {
    "id": str(uuid.uuid4()),
    "user_email": "p.picczy@gmail.com",
    "product": "Jelly",
    "quantity": 1,
}


channel.basic_publish(
    exchange="order",
    routing_key="order.notify",  # key order.notify
    body=json.dumps({"user_email": order["user_email"]}),
)
print("[x] Sent notify message")

channel.basic_publish(
    exchange="order",
    routing_key="order.report",
    body=json.dumps(order),  # ข้อมูลทั้งหมดใน order key="order.report"
)
print("[x] Sent report message")

connection.close()