import uvicorn
from fastapi import FastAPI

from city_data import router as city_router
from degree import router as temperature_router


app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def root() -> dict:
    return {"Server status": "running",
            "Endpoint 1": "/cities/",
            "Endpoint 2": "/city/name/{city_name}",
            "Endpoint 3": "/cities/{city_id} or /city/id/{city_id}",
            }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
