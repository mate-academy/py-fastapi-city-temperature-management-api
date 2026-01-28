from fastapi import FastAPI

from db.session import engine
from db.base import Base
from api.routers.cities import router as cities_router
from api.routers.temperatures import router as temperatures_router

def create_app() -> FastAPI:
    app = FastAPI(title="City Temperature API")

    # create tables
    Base.metadata.create_all(bind=engine)

    app.include_router(cities_router)
    app.include_router(temperatures_router)
    return app

app = create_app()
