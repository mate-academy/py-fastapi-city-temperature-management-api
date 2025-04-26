from fastapi import FastAPI

# from cheese import router as cheese_router
from city import router as city_router
from weather import router as weather_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(weather_router.router)

@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
