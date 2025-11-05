from fastapi import FastAPI
from weather.router import router as city_temperature_router


app = FastAPI(title="City Temperature API")

app.include_router(city_temperature_router)


@app.get("/")
async def root():
    return {"message": "City Temperature API is running!"}
