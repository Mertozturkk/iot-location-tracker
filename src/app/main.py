import asyncio
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from starlette.responses import RedirectResponse
from src.app.config.config import settings
from src.app.api.routes import router as devices_router
from src.app.database.base import Base
from src.app.utils.consumer import consumer
from src.app.utils.tcp_server import start_server

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(devices_router)
Base.metadata.create_all(bind=create_engine(settings.DATABASE_URL))


# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")


def start_consumer():
    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.start()


def start_tcp_server_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_thread = threading.Thread(target=loop.run_until_complete, args=(start_server(),))
    server_thread.start()


@app.on_event("startup")
async def startup_event():
    start_consumer()
    start_tcp_server_thread()
