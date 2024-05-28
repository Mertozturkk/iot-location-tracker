import socket
import asyncio
from src.app.utils.queue import enqueue_data


async def handle_client(reader, writer):
    try:
        data = await reader.read(100)
        print(f"Received: {data.decode()}")
        message = data.decode()
        enqueue_data(message)
        writer.write(data)
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
