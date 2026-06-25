import uvicorn
from fastapi import FastAPI

from app.routers import city, temperature

app = FastAPI(
    title="Cities API",
    version="0.1.0",
    description="API for managing cities",
)


app.include_router(city.router)
app.include_router(temperature.router)
