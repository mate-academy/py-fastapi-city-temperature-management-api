from fastapi import FastAPI

from app import models
from app.database import engine, Base
from app.routers import cities, temperatures


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
