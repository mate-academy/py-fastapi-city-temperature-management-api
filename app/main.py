from fastapi import FastAPI
from .database import Base, engine
from .routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)
