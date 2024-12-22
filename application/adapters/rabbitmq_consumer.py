# application/adapters/rabbitmq_consumer.py

import pika
import json

def start_rabbitmq_consumer(connection_params: pika.ConnectionParameters, queue: str, callback):
    """
    RabbitMQ kuyruk tüketicisi. Mesaj geldiğinde callback fonksiyonunu çağırır.
    callback, aldığımız mesajı parse edip domain use case'ine iletebilir.
    """
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    def on_message(ch, method, properties, body):
        data = json.loads(body)
        # data["event_type"] -> ChatMessageReceived veya ChatMessageAnswered vb.
        # callback(data) ile domain'e iletebilirsin
        callback(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue, on_message_callback=on_message)
    print("[*] Waiting for messages.")
    channel.start_consuming()