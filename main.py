from fastapi import FastAPI
from city import router as city_router
from temperature import router as temperature_router


DEFAULT_LIMIT = 3
DEFAULT_OFFSET = 0


app = FastAPI()


app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/", name="City Temperature Management API")
def root() -> dict:
    return {"description": "City Temperature Management API", "version": "1.0"}
