from fastapi import FastAPI

from cities import router as cities_router
from temperature import router as temperature_router

app = FastAPI()

app.include_router(cities_router.router)


app.include_router(temperature_router.router)


@app.get("/")
def root() -> dict:
    return {"Hello": "World"}
