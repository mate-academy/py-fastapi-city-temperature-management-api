from fastapi import FastAPI

from city.router import router as city_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(city_router)



