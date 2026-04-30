from fastapi import FastAPI

from city_data import router

app = FastAPI()

app.include_router(router.router)
