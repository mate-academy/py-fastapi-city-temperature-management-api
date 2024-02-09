from fastapi import FastAPI

from city_app import router as city_router

app = FastAPI()

app.include_router(city_router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}