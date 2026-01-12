from sqlalchemy.orm import Session

from app.routers import cities, temperatures
from app.models import Base
from app.database import SessionLocal, engine

from fastapi import FastAPI


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(cities.router, tags=["Cities"])
app.include_router(temperatures.router, tags=["Temperatures"])


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
