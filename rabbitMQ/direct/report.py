import pika
import json

# This file is Consumer

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


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


channel.basic_consume(on_message_callback=callback, queue="order_report")

print("[*] Waiting for report message. To exist press CTRL+C")

channel.start_consuming()
