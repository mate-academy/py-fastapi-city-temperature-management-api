from fastapi import FastAPI

from cities import router as cities_router
from temperatures import router as temperatures_router


app = FastAPI()

app.include_router(cities_router.router)
app.include_router(temperatures_router.router)


@app.get("/")
def root() -> dict:
    return {
        "message":
            "Welcome to the City Temperature Management API",
        "/cities/": "City List Page",
        "/cities/{city_id}/": "City Detail Page",
        "/temperature/": "Temperature List Page",
    }
