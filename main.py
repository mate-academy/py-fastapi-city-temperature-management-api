from fastapi import FastAPI
from city.router import router as city_router
from temperature.router import router as temp_router
app = FastAPI()


app.include_router(city_router)
app.include_router(temp_router)
