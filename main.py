from fastapi import FastAPI
from city import router as city_router
from temperature import router as temperature_router
from db.engine import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City & Temperature Management API")

app.include_router(city_router.router)
app.include_router(temperature_router.router)

@app.get("/")
def root():
    return {"message": "City & Temperature Management API is running."}
