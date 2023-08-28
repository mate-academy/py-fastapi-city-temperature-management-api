from fastapi import FastAPI
from cities import router as city_router
# from temperatures import router as temperature_router

app = FastAPI()

app.include_router(city_router.router)
# app.include_router(temperature_router.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
