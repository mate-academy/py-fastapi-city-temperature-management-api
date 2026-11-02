from fastapi import FastAPI
from city_temp.database import Base, engine
from city_temp.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature API", version="1.0.0")

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
def root():
  return {"message": "API is running. Go to /docs for Swagger UI."}
