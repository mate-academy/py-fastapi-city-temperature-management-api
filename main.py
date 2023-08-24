from fastapi import FastAPI
from city import routers as city_routers
from temperature import routers as temperature_routers

app = FastAPI()

app.include_router(city_routers.router)
app.include_router(temperature_routers.router)

# alembic revision --autogenerate -m "first migrations"
# alembic upgrade head

# uvicorn main:app --reload


@app.get("/")
def root():
    return {"message": "Hello World"}
