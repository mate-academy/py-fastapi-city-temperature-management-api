from fastapi import FastAPI

from city.routes import router as cities_router
from temperature.routes import router as temperatures_router

app = FastAPI()

api_version_prefix = "/api/v1"

app.include_router(cities_router, prefix=f"{api_version_prefix}/cities", tags=["cities"])
app.include_router(temperatures_router, prefix=f"{api_version_prefix}/temperatures", tags=["temperatures"])
