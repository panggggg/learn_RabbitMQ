import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("topic_report1")
queue_name = queue.method.queue

channel.queue_bind(exchange="order.topic", queue=queue_name, routing_key="*.any")


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print("[x] Notify {}".format(payload["product"]))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("[*] Waiting for report message. To exist press CTRL+C")

channel.start_consuming()