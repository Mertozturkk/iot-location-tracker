import pika
import json
from src.app.database.models import Base, Location, Device
from datetime import datetime
from src.app.database.session import SessionLocal
from src.app.utils.validator import validate_and_prepare_data, project_logger
from src.app.config.config import settings


@validate_and_prepare_data
def save_data_to_db(data):

    """
        Save device and location data to the database.

        Args:
            data (dict): The data to be saved, containing device and location information.
        """

    session = SessionLocal()
    try:
        device = Device(id=data['device_id'], name=data['device_name'], serial_number=data['serial_number'],
                        model=data['model'], is_active=data['is_active'])
        session.add(device)
        session.commit()
        project_logger.info(f"Device saved: {device.name} - {device.serial_number}")

        location = Location(
            device_id=data['device_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            altitude=data['altitude'],
            speed=data['speed'],
            direction=data['direction'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
        session.add(location)
        session.commit()
        project_logger.info(f"Location saved: {location.latitude} - {location.longitude}")

    except Exception as e:
        project_logger.error(f"Error saving data: {e}")
        session.rollback()
    finally:
        session.close()


def callback(ch, method, properties, body):
    """
        Callback function to process received messages.

        Args:
            ch: The channel object.
            method: The method frame with delivery information.
            properties: The properties of the message.
            body (bytes): The body of the message.
        """

    location_data = json.loads(body)
    project_logger.info(f"Received data: {location_data}")
    save_data_to_db(location_data)


def consumer():
    """
        Set up the consumer to receive and process messages from the queue.
    """

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)
    channel.basic_consume(queue=settings.RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    project_logger.debug('Waiting for messages...')
    channel.start_consuming()
