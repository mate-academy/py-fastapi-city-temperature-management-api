from fastapi import FastAPI

from city import router as cities_router
from temperature import router as temperatures_router

app = FastAPI()

app.include_router(cities_router.router)
app.include_router(temperatures_router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
