from fastapi import FastAPI
from city.routes import router as city_router
from temperature.routes import router as temperature_router


app = FastAPI(debug=True)
app.include_router(city_router, prefix="")
app.include_router(temperature_router, prefix="")
