import datetime

from fastapi import HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.app.database.models import Device, Location
from src.app.schemas.device import DeviceCreate
from src.app.database.session import get_db
from src.app.utils.validator import project_logger


def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """
        Create a new device and add a default location.

        Args:
            device (DeviceCreate): The device data to be created.
            db (Session): The database session.

        Returns:
            The created device.

        Raises:
            HTTPException: If the device already exists or any other error occurs.
        """
    try:
        existing_device = db.query(Device).filter(
            (Device.serial_number == device.serial_number) | (Device.name == device.name)).first()
        if existing_device:
            raise HTTPException(status_code=400, detail="Device with this serial number or name already exists")

        db_device = Device(**device.dict())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)

        # Varsayılan konum bilgisi ekleme
        default_location = Location(
            device_id=db_device.id,
            latitude=0.0,
            longitude=0.0,
            altitude=0.0,
            speed=0.0,
            direction=0.0,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(default_location)
        db.commit()
        db.refresh(default_location)

    except IntegrityError as e:
        db.rollback()
        project_logger.error(f"IntegrityError creating device: {e}")
        raise HTTPException(status_code=400, detail="Device with this serial number or name already exists")
    except Exception as e:
        db.rollback()
        project_logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail="Error creating device")

    project_logger.info(f"Device created: {db_device}")
    return db_device


def get_devices(db: Session, skip: int = 0, limit: int = 10):
    """
        Retrieve a list of devices with optional pagination.

        Args:
            db (Session): The database session.
            skip (int): The number of records to skip.
            limit (int): The maximum number of records to return.

        Returns:
            List of devices.

        Raises:
            HTTPException: If any error occurs during the retrieval.
        """

    try:
        db_devices = db.query(Device)
        if skip:
            db_devices = db_devices.offset(skip)
        if limit:
            db_devices = db_devices.limit(limit)
    except Exception as e:
        project_logger.error(f"Error reading devices: {e}")
        raise HTTPException(status_code=500, detail="Error reading devices")

    project_logger.info(f"Devices read: {db_devices}")
    return db_devices.all()


def delete_device(db: Session, device_id: int):
    """
        Delete a device by its ID.

        Args:
            db (Session): The database session.
            device_id (int): The ID of the device to be deleted.

        Returns:
            A message indicating successful deletion.

        Raises:
            HTTPException: If the device is not found or any other error occurs.
        """
    try:
        db_device = db.query(Device).filter(Device.id == device_id).first()
        if db_device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        db.delete(db_device)
        db.commit()
    except Exception as e:
        project_logger.error(f"Error deleting device: {e}")
        raise HTTPException(status_code=500, detail="Error deleting device")

    project_logger.info(f"Device deleted: {db_device}")
    return {"message": "Device deleted"}


def get_device_locations(db: Session, device_id: int, skip: int = 0, limit: int = 100):
    """
        Retrieve locations for a specific device with optional pagination.

        Args:
            db (Session): The database session.
            device_id (int): The ID of the device.
            skip (int): The number of records to skip.
            limit (int): The maximum number of records to return.

        Returns:
            List of locations for the specified device.

        Raises:
            HTTPException: If any error occurs during the retrieval.
        """
    try:
        db_locations = db.query(Location).filter(Location.device_id == device_id)
        if skip:
            db_locations = db_locations.offset(skip)
        if limit:
            db_locations = db_locations.limit(limit)
    except Exception as e:
        project_logger.error(f"Error reading locations: {e}")
        raise HTTPException(status_code=500, detail="Error reading locations")
    project_logger.info(f"Locations read: {db_locations}")
    return db_locations.all()


def get_last_location_for_all_devices(db: Session = Depends(get_db)):
    """
        Retrieve the last known location for all devices.

        Args:
            db (Session): The database session.

        Returns:
            List of the last known locations for all devices.

        Raises:
            HTTPException: If any error occurs during the retrieval.
        """
    try:
        subquery = db.query(Location.device_id, func.max(Location.timestamp).label("max_timestamp")).group_by(
            Location.device_id).subquery()
        last_locations = db.query(Location).join(subquery, (Location.device_id == subquery.c.device_id) & (
                    Location.timestamp == subquery.c.max_timestamp)).all()
    except Exception as e:
        project_logger.error(f"Error getting last locations: {e}")
        raise HTTPException(status_code=500, detail="Error getting last locations")
    project_logger.info(f"Last locations read: {last_locations}")
    return last_locations
