from fastapi import FastAPI

from weather.router import router as cities_router
from temperature.router import router as temperature_router

app = FastAPI()

app.include_router(
    router=cities_router, prefix="/weather", tags=["Cities"]
)
app.include_router(
    router=temperature_router, prefix="/temperature", tags=["Temperature"]
)


@app.get("/",)
def read_root() -> dict:
    return {"message": "Hello World"}
