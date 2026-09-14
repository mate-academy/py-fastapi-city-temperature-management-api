from fastapi import FastAPI

from City import router as CityRouter
from Temperature import router as TemperatureRouter

app = FastAPI()

app.include_router(CityRouter.router)
app.include_router(TemperatureRouter.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
