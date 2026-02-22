from fastapi import FastAPI


from app.routers.cities_api import router as cities_router
from app.routers.temperature_api import router as temperature_router

app = FastAPI()

app.include_router(cities_router)
app.include_router(temperature_router)


@app.get("/")
def root():
    return {"message": "HELLO TO MY API"}