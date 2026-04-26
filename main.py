from fastapi import FastAPI
from database import Base, engine
from city.routers import city
from temperature.routers import temperature
from city import models as city_models
from temperature import models as temperature_models

app = FastAPI()

app.include_router(city.router)
app.include_router(temperature.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> dict:
    return {"Hello": "World!"}
