from fastapi import FastAPI
from app.routers import (
    city_routers,
    temperature_routers
)


app = FastAPI()

app.include_router(city_routers.router, prefix="/api")
app.include_router(temperature_routers.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Weather API"}
