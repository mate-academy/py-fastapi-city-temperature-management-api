from fastapi import FastAPI

from core.config import settings
from routers import city, temperature

app = FastAPI(
    title="Weather Monitor API",
    version="1.0.0",
    description="API for temperature monitoring in cities",
)

app.include_router(city.router, prefix=settings.API_V1_PREFIX)
app.include_router(temperature.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Weather API",
        "docs": "/docs"
    }
