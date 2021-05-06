import pika
import json

# This file is Consumer

# connect rabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print("[x] Notify {}".format(payload["user_email"]))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="order_notify", on_message_callback=callback)


print("[*] Waiting for notify message. To exist press CTRL + C")

channel.start_consuming()