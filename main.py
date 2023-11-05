from fastapi import FastAPI

from city import router as cities_router

app = FastAPI()

app.include_router(cities_router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
