import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("fanout_report1")
queue_name = queue.method.queue

channel.queue_bind(exchange="order.fanout", queue=queue_name, routing_key="")


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print("[x] Generating report")
    print(
        f"""
        ID: {payload.get('id')}
        User Email: {payload.get('user_email')}
        Product: {payload.get('product')}
        Quantity: {payload.get('quantity')}
        """
    )
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("[*] Waiting for report message. To exist press CTRL+C")

channel.start_consuming()