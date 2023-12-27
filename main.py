from typing import Union

from fastapi import FastAPI

from city.router import router as city_router

app = FastAPI()

app.include_router(city_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
