import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/iot_db")
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI")
    VERSION: str = os.getenv("VERSION", "0.1.0")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://user:password@localhost")
    RABBITMQ_QUEUE: str = os.getenv("RABBITMQ_QUEUE", "iot_queue")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")

settings = Settings()
