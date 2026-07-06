from fastapi import FastAPI

from project.database import Base, engine
from project.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)
