from fastapi import FastAPI

import models
from database import engine
from cities.router import router as cities_router
from temperatures.router import router as temperatures_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather & Cities Management API",
    description="Модульний REST API сервіс для управління містами та асинхронного завантаження температур",
    version="1.0.0",
)

app.include_router(cities_router)
app.include_router(temperatures_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Weather API. Go to /docs for interactive API documentation."
    }