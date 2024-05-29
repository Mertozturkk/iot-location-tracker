from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from starlette.responses import RedirectResponse
from src.app.config.config import settings
from src.app.api.routes import router as devices_router
from src.app.database.base import Base
from src.app.utils.consumer import consumer

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
consumer()

# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")
