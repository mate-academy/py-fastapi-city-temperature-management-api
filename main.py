from fastapi import FastAPI, APIRouter
from cities.routes import router as cities_router
from temperature.routes import router as temperature_router

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(cities_router)
app.include_router(temperature_router)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Welcome to the City Temperature API"}
