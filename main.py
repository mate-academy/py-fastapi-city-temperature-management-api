from fastapi import FastAPI

from temperatures.router import router as temp_router
from cities.router import router as city_router


app = FastAPI()
app.include_router(temp_router)
app.include_router(city_router)


@app.get("/")
async def root() -> dict:
    return {"message": "City and Temperature API"}
