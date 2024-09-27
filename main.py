from fastapi import FastAPI
from city import router as city_router
from temperature import router as temperature_router

app = FastAPI(
    title="City Temperature Management",
    description="Operations related to city temperature management.",
    version="1.0.0",
)

app.include_router(city_router.router)
app.include_router(temperature_router.router)
