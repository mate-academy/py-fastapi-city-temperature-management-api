from fastapi import FastAPI, Depends

from city_crud_api.router import city_router
from dependencies import get_db
from temperature_api.router import temperature_router

app = FastAPI()


@app.get("/")
def hello():
    return "Hello!"

app.include_router(city_router, dependencies=[Depends(get_db)])
app.include_router(temperature_router, dependencies=[Depends(get_db)])
