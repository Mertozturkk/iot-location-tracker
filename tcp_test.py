import itertools
import socket
import json
import random
import time
import datetime

device_id_counter = itertools.count(1)


def generate_random_device_id():
    return next(device_id_counter)


def generate_random_location_data(device_id):
    return {
        "device_id": device_id,
        "device_name": f"Device {device_id}",
        "serial_number": f"SN{device_id:05d}",
        "model": f"Model_{random.randint(1, 100)}",
        "is_active": random.choice([True, False]),
        "created_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat(),
        "latitude": random.uniform(-90.0, 90.0),
        "longitude": random.uniform(-180.0, 180.0),
        "altitude": random.uniform(0, 10000),
        "speed": random.uniform(0, 120),
        "direction": random.uniform(0, 360),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


def send_data_to_tcp_server(data, host='127.0.0.1', port=8888):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            json_data = json.dumps(data) + '\n'
            print(f"Sending data: {json_data}")
            sock.sendall(json_data.encode('utf-8'))
            received = sock.recv(1024)
            print("Received:", received.decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    while True:
        for _ in range(10):
            device_id = generate_random_device_id()
            data = generate_random_location_data(device_id)
            send_data_to_tcp_server(data)
            time.sleep(6)
