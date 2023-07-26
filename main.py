from fastapi import FastAPI

from city_api.router import city_router
from temperature_api.router import temp_router



app = FastAPI()

app.include_router(city_router)
app.include_router(temp_router)

@app.get("/")
def root() -> dict:
    return {"message": "apps main page"}