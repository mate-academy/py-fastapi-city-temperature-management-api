from fastapi import FastAPI
import models
from database import engine
from routers import cities, temperatures

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)
