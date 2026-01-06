from fastapi import FastAPI
from city.router import router as city_router
from temperature.router import router as temperature_router
from settings import settings


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def read_root():
    return {"message": "City Temperature Management API is running!"}
