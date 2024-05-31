from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.app.database.session import get_db
from src.app.schemas import device as schemas
from src.app.utils import device as crud
from src.app.utils.validator import project_logger

router = APIRouter(
    prefix='/devices',
    tags=['devices']
)


@router.post("/", response_model=schemas.DeviceResponse)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """
    Create a new device.

    - **name**: Name of the device
    - **serial_number**: Serial number of the device
    - **model**: Model of the device
    - **is_active**: Activation status of the device (optional, default is True)
    """
    project_logger.info(f"Received request to create device: {device}")
    return crud.create_device(db=db, device=device)


@router.get("/", response_model=list[schemas.DeviceResponse])
def read_devices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        List all devices with pagination.

        - **skip**: Number of devices to skip (optional, default is 0)
        - **limit**: Maximum number of devices to return (optional, default is 10)
        """
    project_logger.info(f"Received request to read devices with skip={skip} and limit={limit}")
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices


@router.delete("/{device_id}", response_model=schemas.DeviceResponse)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """
        Delete a device by its ID.

        - **device_id**: ID of the device to be deleted
        """
    project_logger.info(f"Received request to delete device with ID: {device_id}")
    return crud.delete_device(db=db, device_id=device_id)


@router.get("/{device_id}/locations", response_model=list[schemas.LocationResponse])
def read_device_locations(device_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List location history for a specific device.

    - **device_id**: ID of the device
    """
    project_logger.info(f"Received request to read locations for device with ID: {device_id}")
    return crud.get_device_locations(db, device_id=device_id, skip=skip, limit=limit)


@router.get("/last_locations", response_model=list[schemas.LocationResponse])
def get_last_locations(db: Session = Depends(get_db)):
    """
        Get the last known location for all devices.
        """
    project_logger.info(f"Received request to get last known locations for all devices")
    return crud.get_last_location_for_all_devices(db=db)

