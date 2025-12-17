from fastapi import FastAPI
from city.router import router

app = FastAPI(title="City Temperature Management API")

app.include_router(router)
