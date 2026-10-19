from fastapi import FastAPI

import city

app = FastAPI()

app.include_router(city.router)
# app.include_router(temperature.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}