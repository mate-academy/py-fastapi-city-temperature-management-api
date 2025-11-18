from fastapi import FastAPI
from app.routers import cities, temperatures
from app.db import init_db


app = FastAPI(title="Cities & Temperatures API")


app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])


@app.on_event("startup")
def on_startup():
    init_db()
