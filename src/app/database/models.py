import datetime
from sqlalchemy import Column, String, Float, ForeignKey, Boolean, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from src.app.database.base import Base


class Device(Base):
    __tablename__ = 'devices'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    serial_number = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    locations = relationship('Location', order_by='Location.timestamp', back_populates='device',
                             cascade="all, delete-orphan")


class Location(Base):
    __tablename__ = 'locations'
    id = Column(BigInteger, primary_key=True, index=True)
    device_id = Column(BigInteger, ForeignKey('devices.id'), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    direction = Column(Float, nullable=True)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow, index=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    device = relationship('Device', back_populates='locations')


Device.locations = relationship('Location', order_by=Location.id, back_populates='device', cascade="all, delete-orphan")
