from fastapi import FastAPI

from src.city.models import City  # noqa: F401
from src.city.router import router as city_router
from src.database import Base, engine
from src.temperature.models import Temperature  # noqa: F401
from src.temperature.router import router as temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")

app.include_router(city_router)
app.include_router(temperature_router)
