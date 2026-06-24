from fastapi import FastAPI

from database import Base, engine

from city import models as city_models  # noqa: F401
from temperature import models as temperature_models  # noqa: F401

from city.router import router as city_router
from temperature.router import router as temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather App")

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def root():
    return {"message": "Weather App. See /docs for the API."}