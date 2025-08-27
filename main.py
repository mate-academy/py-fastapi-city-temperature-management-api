from fastapi import FastAPI

from city.routes import city
from temperature.routes import temperature

app = FastAPI()
app.include_router(city)
app.include_router(temperature)

@app.get("/")
async def read_root():
    return {"message": "Hello. This is city temperature service!"}
