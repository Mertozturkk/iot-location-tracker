import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI")
    VERSION: str = os.getenv("VERSION", "0.1.0")

settings = Settings()
