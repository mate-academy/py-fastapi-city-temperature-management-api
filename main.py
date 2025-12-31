# main.py
from fastapi import FastAPI

from city_crud_api import router as city_router
from temperature_api import router as temperature_router


# Create a FastAPI app instance
app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)
# Define a path operation decorator for a GET request at the root URL ("/")
@app.get("/")
def read_root():
    """
    A simple path operation function that returns a JSON message.
    """
    return {"Hello": "World"}
