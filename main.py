from fastapi import FastAPI

from city_temperature import router as city_temperature_router


app = FastAPI()

app.include_router(city_temperature_router.router)
