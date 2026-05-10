from fastapi import FastAPI
from app.api import cities, temperatures

app = FastAPI(title="City Weather API")

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
async def root():
    return {"message": "Welcome to City Weather API"}
