import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.main import app
from src.app.database.base import Base
from src.app.database.session import get_db
from src.app.config.config import settings

engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_device_with_default_location():
    response = client.post(
        "/devices/",
        json={"name": "Device 1 ", "serial_number": "SN3438", "model": "Model 4", "is_active": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Device3"
    assert data["serial_number"] == "SN3448"
    assert data["model"] == "Model 4"
    assert data["is_active"] is True

    device_id = data["id"]
    response = client.get(f"/devices/{device_id}/locations/")
    assert response.status_code == 200
    location_data = response.json()
    assert location_data[0]["latitude"] == 0.0
    assert location_data[0]["longitude"] == 0.0


def test_delete_device():
    response = client.post(
        "/devices/",
        json={"name": "Test Device 132", "serial_number": "SN1215274", "model": "Model 1", "is_active": True},
    )
    assert response.status_code == 200
    data = response.json()
    device_id = data["id"]

    response = client.delete(f"/devices/{device_id}")
    assert response.status_code == 200



def test_list_devices():
    response = client.get("/devices/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_location_history():
    response = client.post(
        "/devices/",
        json={"name": "Test Device for Location1", "serial_number": "SN122347", "model": "Model 3", "is_active": True},
    )
    assert response.status_code == 200
    data = response.json()
    device_id = data["id"]

    response = client.get(f"/devices/{device_id}/locations/")
    assert response.status_code == 200
    data = response.json()


def test_get_last_location_for_all_devices():
    response = client.get("/devices/last_locations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
