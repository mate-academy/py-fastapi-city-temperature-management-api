from fastapi import FastAPI

from app import models  # noqa: F401
from app.database import Base, engine
from app.routers import cities, temperatures


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='City Temperature API',
    description='API for managing cities and temperature history',
    version='1.0.0',
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get('/')
def root() -> dict[str, str]:
    return {'message': 'City Temperature API is running'}
