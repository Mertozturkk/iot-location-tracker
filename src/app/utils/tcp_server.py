import socket
import asyncio
import json
from src.app.utils.queue import enqueue_data


async def handle_client(reader, writer):
    try:
        data = await reader.readuntil(separator=b'\n')
        message = data.decode().strip()
        print(f"Received message: {message}")
        try:
            json_data = json.loads(message)
            enqueue_data(json_data)
            writer.write(b"Data received\n")
            await writer.drain()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            writer.write(b"Invalid JSON format\n")
            await writer.drain()
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        writer.close()


async def start_server():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start_server())
