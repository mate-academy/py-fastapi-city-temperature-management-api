from fastapi import FastAPI


from app.city.router import router as city_router
from app.temperature.router import router as temp_router

app = FastAPI()


app.include_router(city_router, prefix="/city")
app.include_router(temp_router, prefix="/temperatures")


@app.get("/")
async def root():
    return {"message": "City and Temperature Management API"}
