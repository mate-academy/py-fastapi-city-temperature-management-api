from fastapi import FastAPI

from city import router as city_router

app = FastAPI()

app.include_router(city_router.router)
# app.include_router(temperature.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}