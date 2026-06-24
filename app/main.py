from fastapi import FastAPI
from app.database import engine, Base
from app.routers import cities, temperatures

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])