from fastapi import FastAPI

from temperature import router as temperature_router
from city import router as city_router

app = FastAPI()

app.include_router(temperature_router.router)
app.include_router(city_router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
