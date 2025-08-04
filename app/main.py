from fastapi import FastAPI

from routes import temperatures_router, city_router

app = FastAPI()

app.include_router(city_router, tags=["Cities"])
app.include_router(temperatures_router, tags=["Temperatures"])
