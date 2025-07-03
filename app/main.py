import os

from dotenv import load_dotenv
from fastapi import FastAPI
from .database import Base, engine
from .routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature API")

app.include_router(cities.router, prefix="/cities")
app.include_router(temperatures.router, prefix="/temperatures")

@app.get("/")
def root():
    return {"message": "Welcome to the City Temperature API!"}
