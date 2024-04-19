from fastapi import FastAPI

from city.router import router as city_router
from temperature.router import router as temperature_router


app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def index():
    return {
        "Docs": "/docs/",
        "All cities": app.url_path_for("read_all_cities"),
        "Add new city": app.url_path_for("create_city"),
        "All temperature records": app.url_path_for("read_temperature_records"),
        "Fetch temperature for all cities": app.url_path_for(
            "fetch_temperature_for_all_cities"
        ),
    }
