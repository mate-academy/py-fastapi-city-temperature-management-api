from fastapi import FastAPI

from cities.routers import city_router

from temperatures.routers import temperature_routers

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_routers)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World !"}
