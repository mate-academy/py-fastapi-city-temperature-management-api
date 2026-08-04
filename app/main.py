from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers.cities import router as cities_router
from app.routers.temperatures import (
    router as temperatures_router,
)


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(cities_router)
app.include_router(temperatures_router)
