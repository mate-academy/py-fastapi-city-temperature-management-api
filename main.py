from fastapi import FastAPI

from city import router as city_router
from settings import settings
from temperature import router as temperature_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
async def root() -> dict:
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "endpoints": {
            "cities": {
                "GET /cities": "Get a list of all cities",
                "POST /cities": "Create a new city",
                "GET /cities/{city_id}": "Get the details of a specific city",
                "PUT /cities/{city_id}": "Update the details of a specific city",
                "DELETE /cities/{city_id}": "Delete a specific city"
            },
            "temperatures": {
                "GET /temperatures": "Get a list of all temperature records",
                "GET /temperatures/?city_id={city_id}": "Get temperature records for a specific city",
                "POST /temperatures/update": "Fetch and store current temperatures for all cities"
            }
        }
    }
