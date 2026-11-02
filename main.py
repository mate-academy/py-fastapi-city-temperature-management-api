from fastapi import FastAPI

from cities import router as cities_router
from database import engine, Base
from temperatures import router as temperatures_router

app = FastAPI(title="City Temperature API")

app.include_router(cities_router.router)
app.include_router(temperatures_router.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "City Temperature API is running"}