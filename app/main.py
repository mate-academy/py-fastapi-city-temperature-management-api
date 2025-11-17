from fastapi import FastAPI

from app.database import engine, Base
from app.routers.city import router as city_router
from app.routers.temperature import router as temperature_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root() -> dict:
    return {"message": "Hello"}


app.include_router(city_router)
app.include_router(temperature_router)