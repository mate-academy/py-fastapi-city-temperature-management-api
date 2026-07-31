from fastapi import FastAPI
from city.router import router

app = FastAPI()
app.include_router(router)
