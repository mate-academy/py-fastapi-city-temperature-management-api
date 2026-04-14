from fastapi import FastAPI

from city_api import city_router
from temperature_api import temperature_router

app = FastAPI(
    title="City Temperature Management API",
    description="FastAPI application that manages city data and their corresponding temperature data."
)


app.include_router(city_router, tags=["city"])
app.include_router(temperature_router, tags=["temperature"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
