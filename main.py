from fastapi import FastAPI

from city import city_router
from temperature import temperature_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
