from fastapi import FastAPI
from routers import cities, temperatures
from db import models, database


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(cities.router)
app.include_router(temperatures.router)


