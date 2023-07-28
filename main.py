from fastapi import FastAPI

from city import router as city_router
from temperature_api import router as temperature_router

app = FastAPI(debug=True)

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
