from fastapi import FastAPI

from app.database import Base
from app.database import engine
from app.routers.cities import router as city_router
from app.routers.temperatures import router as temperature_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)
