from fastapi import FastAPI

from app.routers import city, temperature

app = FastAPI()

app.include_router(city.router, prefix="/cities", tags=["cities"])
app.include_router(
    temperature.router,
    prefix="/temperatures",
    tags=["temperatures"]
)
