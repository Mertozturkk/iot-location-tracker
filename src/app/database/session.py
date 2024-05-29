from sqlalchemy.orm import sessionmaker
from src.app.config.config import settings
from sqlalchemy import create_engine

# create a Session
engine = create_engine( settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()