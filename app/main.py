from fastapi import FastAPI
from app.api import city, temperature
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city.router)
app.include_router(temperature.router)
