import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/iot_db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost/test_db")
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI")
    VERSION: str = os.getenv("VERSION", "0.1.0")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://user:password@localhost")
    RABBITMQ_QUEUE: str = os.getenv("RABBITMQ_QUEUE", "iot_queue")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


settings = Settings()
