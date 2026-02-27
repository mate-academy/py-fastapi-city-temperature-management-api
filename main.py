from fastapi import FastAPI

from city_temp.routers import cities, temps
from database import engine, Base
from settings import settings


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(cities.router)
app.include_router(temps.router)


@app.get("/")
def main():
    return {"status": "ok"}
