from fastapi import FastAPI

from app.database import init_db
from routers.cities import router as cities_router
from routers.temperatures import router as temperatures_router

app = FastAPI()

app.include_router(cities_router, prefix="/api")
app.include_router(temperatures_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    init_db()
