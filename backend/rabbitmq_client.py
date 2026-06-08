# backend-core/rabbitmq_client.py
import os

import pika
import json

def publish_to_rabbitmq(message_data):
    try:
        rabbitmq_url = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq-service:5672')
        
        parameters = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='contact_requests', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='contact_requests',
            body=json.dumps(message_data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        connection.close()
        print("Message published to RabbitMQ successfully!")
    except Exception as e:
        print(f"Failed to publish to RabbitMQ: {e}")