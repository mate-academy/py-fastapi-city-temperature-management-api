from fastapi import FastAPI

from src.city.router import city_router

from src.database import Base, engine
from src.temperature.router import temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(temperature_router)
app.include_router(city_router)


@app.get("/")
def home():
    return {"message": "Home Page"}
