from fastapi import FastAPI
import models
from database import engine
from routers import cities, temperatures
import os

from dotenv import load_dotenv
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature API")

app.include_router(cities.router)
app.include_router(temperatures.router)
