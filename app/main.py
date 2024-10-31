from fastapi import FastAPI

from . import models, database
from .routers import city, temperature

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(city.router)
app.include_router(temperature.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the City Temperature Management API"}
