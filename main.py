from fastapi import FastAPI
from city.router import router as city_router
from temperature.router import router as temperature_router

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def root() -> dict:
    return {
        "endpoints": "/cities/, /cities/{city_id}, /temperatures/, "
                     "/temperatures/?city_id={city_id}, /temperatures/update/"
    }
