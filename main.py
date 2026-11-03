from fastapi import FastAPI
from city.router import router
from temperature.router import router as temperature_router

app = FastAPI()

app.include_router(router)
app.include_router(temperature_router)


@app.get('/')
async def root():
    return {"message": "Hello world"}
