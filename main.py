from fastapi import FastAPI

from api import cities, temperature

app = FastAPI()


app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(temperature.router, prefix="/temperatures", tags=["temperatures"])
