from fastapi import FastAPI

from management.routers import city_routers, temperature_routers

app = FastAPI()


app.include_router(city_routers.router)
app.include_router(temperature_routers.router)
