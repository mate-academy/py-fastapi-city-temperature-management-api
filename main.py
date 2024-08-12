from fastapi import FastAPI

app = FastAPI()

from city_app.router import router as city_router
from temperature_app.router import router as temperature_router

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def root() -> dict:
    return {"Hello": "World"}
