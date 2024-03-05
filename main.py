from fastapi import FastAPI

from city.routers import router

app = FastAPI()


app.include_router(router)
