import pika
import json
from src.app.utils.validator import project_logger
from src.app.config.config import settings


def get_connection():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials)
    )
    return connection


def enqueue_data(data):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)

    message = json.dumps(data)
    project_logger.debug(f"Enqueueing data: {message}")
    channel.basic_publish(exchange='',
                          routing_key=settings.RABBITMQ_QUEUE,
                          body=message)
    connection.close()
