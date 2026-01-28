from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers import cities, temperatures

app = FastAPI(title="City Temperature API")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/")
async def root():
    return {"status": "ok"}
