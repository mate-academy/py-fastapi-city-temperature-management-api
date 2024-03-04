from fastapi import FastAPI

from city import router as city_router
from temperature import router as temperature_router


app = FastAPI(title="Module Python Core/FastAPI in Details",
              description="Task 'py-fastapi-city-temperature-management-api'",
              summary="FastAPI application that manages city data and their corresponding temperature data")
app.include_router(city_router.router)
app.include_router(temperature_router.router)




