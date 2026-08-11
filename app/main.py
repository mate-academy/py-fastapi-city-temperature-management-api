from fastapi import FastAPI

from app.routers import cities, temperatures


app = FastAPI(
    title="City Temperature Management API"
)

app.include_router(cities.router)
app.include_router(temperatures.router)
