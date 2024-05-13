import uvicorn

from fastapi import FastAPI

from app.city import router as city_routers
from app.temperature import router as temperature_routers


app = FastAPI()

app.include_router(city_routers.router)
app.include_router(temperature_routers.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
