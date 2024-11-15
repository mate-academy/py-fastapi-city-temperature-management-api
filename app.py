from fastapi import FastAPI
from cities.router import router as cities_router
from temperatures.router import router as temperatures_router


app = FastAPI()

app.include_router(cities_router)
app.include_router(temperatures_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
