from fastapi import FastAPI
from app.cities.routes import router as cities_router
from app.temperatures.routes import router as temperatures_router
from app.database import Base, engine

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cities_router, prefix="/cities")
app.include_router(temperatures_router, prefix="/temperatures")
