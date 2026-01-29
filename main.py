from fastapi import FastAPI

from routers import city, temperature

app = FastAPI()

app.include_router(city.router)
app.include_router(temperature.router)
