from fastapi import FastAPI


from city.urls import router as city_router
from temperature_api.urls import router as temp_router

app = FastAPI()

app.include_router(city_router, tags=["cities"])
app.include_router(temp_router, tags=["temperatures"])
