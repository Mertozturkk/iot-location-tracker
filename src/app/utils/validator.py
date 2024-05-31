import logging
from functools import wraps
from datetime import datetime
from src.app.config.config import settings


def setup_logger(name, level=logging.INFO):
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)

    return logger


project_logger = setup_logger('project_logger', level=getattr(logging, settings.LOG_LEVEL))


def validate_and_prepare_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = args[0]
        errors = []
        warnings = []

        if 'device_id' not in data or not isinstance(data['device_id'], int):
            errors.append("Invalid or missing 'device_id'.")

        if 'device_name' not in data or not isinstance(data['device_name'], str):
            errors.append("Invalid or missing 'device_name'.")

        if 'serial_number' not in data or not isinstance(data['serial_number'], str):
            data['serial_number'] = None
            warnings.append("Missing 'serial_number', setting it to None.")

        if 'model' not in data or not isinstance(data['model'], str):
            data['model'] = None
            warnings.append("Missing 'model', setting it to None.")

        if 'is_active' not in data or not isinstance(data['is_active'], bool):
            data['is_active'] = True
            warnings.append("Missing 'is_active', setting it to True.")

        if 'latitude' not in data or not isinstance(data['latitude'], (int, float)):
            errors.append("Invalid or missing 'latitude'.")

        if 'longitude' not in data or not isinstance(data['longitude'], (int, float)):
            errors.append("Invalid or missing 'longitude'.")

        if 'timestamp' not in data:
            errors.append("Missing 'timestamp'.")
        else:
            try:
                datetime.fromisoformat(data['timestamp'])
            except ValueError:
                errors.append("Invalid 'timestamp' format.")

        if errors:
            project_logger.error("Data validation errors: %s", errors)
            return False

        if warnings:
            project_logger.warning("Data validation warnings: %s", warnings)
            send_warning_to_system(warnings)

        return func(*args, **kwargs)

    return wrapper


def send_warning_to_system(warnings):
    project_logger.warning("Sisteme uyarılar gönderildi:", warnings)
