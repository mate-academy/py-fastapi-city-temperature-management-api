from fastapi import FastAPI

from app.routers import cities, temperatures

app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
async def root():
    return {"message": "Weather API is running"}