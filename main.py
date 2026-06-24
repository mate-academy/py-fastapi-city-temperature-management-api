from fastapi import FastAPI
from database import engine, Base
from city.router import router as city_router
from temperature.router import router as temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)
