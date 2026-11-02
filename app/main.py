from fastapi import FastAPI

from app.city import models as city_models  # noqa: F401
from app.city.router import router as city_router
from app.database import Base, engine
from app.temperature import models as temperature_models  # noqa: F401
from app.temperature.router import router as temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather API")

app.include_router(city_router)
app.include_router(temperature_router)
