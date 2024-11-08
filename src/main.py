from fastapi import FastAPI
from src.city import routers as city_routers
from src.temperature import routers as temperature_routers


app = FastAPI()
app.include_router(city_routers.router)
app.include_router(temperature_routers.router)


@app.get("/")
async def main_page():
    return "Hello world!"
