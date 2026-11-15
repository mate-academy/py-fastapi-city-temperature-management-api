from fastapi import FastAPI

from app.cities import models as city_models  # noqa: F401
from app.cities.router import router as cities_router
from app.database import Base, engine
from app.temperatures import models as temperature_models  # noqa: F401
from app.temperatures.router import router as temperatures_router

print(Base.metadata.tables.keys())
Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature API")
app.include_router(cities_router)
app.include_router(temperatures_router)