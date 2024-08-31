from fastapi import FastAPI

from city.router import city_router
from temperature.router import temperature_router


app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to City temperature API!"}
