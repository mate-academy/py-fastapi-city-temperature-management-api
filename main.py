from fastapi import FastAPI

from city_crud_api.api.router import router as city_router

app = FastAPI()

app.include_router(city_router)