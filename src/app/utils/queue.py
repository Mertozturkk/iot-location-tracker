import pika
import json
from src.app.utils.validator import project_logger


def get_connection():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials)
    )
    return connection


def enqueue_data(data):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='iot_queue')

    message = json.dumps(data)
    project_logger.debug(f"Enqueueing data: {message}")
    channel.basic_publish(exchange='',
                          routing_key='iot_queue',
                          body=message)
    connection.close()
