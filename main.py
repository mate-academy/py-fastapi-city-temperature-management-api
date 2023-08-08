from fastapi import FastAPI

from cities import city_router
from temperatures import temperature_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Welcome!"}
