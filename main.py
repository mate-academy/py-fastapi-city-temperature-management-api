from fastapi import FastAPI

from city.routers import router
from temperature.routers import router_temp

app = FastAPI()
app.include_router(router, prefix="/cities", tags=["cities"])
app.include_router(router_temp, prefix="/temperatures", tags=["temperatures"])

@app.get("/")
async def root():
    return {"message": "Welcome to the City Temperature API"}
