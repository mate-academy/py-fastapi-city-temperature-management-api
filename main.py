from fastapi import FastAPI

from database import Base, engine
from cities.router import router as cities_router
from temperatures.router import router as temperatures_router

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {"status": "ok"}


app.include_router(cities_router)
app.include_router(temperatures_router)


