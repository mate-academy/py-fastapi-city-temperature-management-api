from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import cities, temperatures


app = FastAPI(
    title="City Temperature API",
    description="API for managing cities and temperature history",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(cities.router)
app.include_router(temperatures.router)