from fastapi import FastAPI
from routes.city import router as city_router
from routes.temperature import router as temperature_router

app = FastAPI(
    title="City Temperature Management API",
    description="API for managing cities and their temperature records",
    version="1.0.0",
)


@app.get("/")
async def read_root():
    return {
        "message": "City Temperature Management API",
        "endpoints": {
            "cities": "/cities",
            "temperatures": "/temperatures",
            "docs": "/docs",
        },
    }


app.include_router(city_router)
app.include_router(temperature_router)
