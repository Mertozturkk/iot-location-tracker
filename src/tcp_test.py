import socket
import json


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
    data = {
        "device_id": "1",
        "device_name": "Test Device",
        "latitude": 40.712776,
        "longitude": -74.005974,
        "timestamp": "2023-05-28T12:34:56"
    }
    send_data_to_tcp_server(data)
