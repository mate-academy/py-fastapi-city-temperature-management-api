from fastapi import FastAPI
from database import Base, engine
from city.routers import router as city_router
from temperature.routers import router as temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)
