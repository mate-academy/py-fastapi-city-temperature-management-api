from fastapi import FastAPI

import cities.router as cities_router
import temperatures.router as temperature_router

app = FastAPI()

app.include_router(cities_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World!"}
