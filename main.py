from fastapi import FastAPI
from db.engine import Base, engine

from routers.cities import router as city_router
from routers.temperatures import router as temperature_router


app = FastAPI(
    title="Temperature Management API",
    description="API for managing cities and temperature history",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def root():
    return {"message": "Database connected"}
