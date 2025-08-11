from fastapi import FastAPI
from .database import Base, engine
from . import city_routes, temperature_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City & Temperature API")

app.include_router(city_routes.router)
app.include_router(temperature_routes.router)
