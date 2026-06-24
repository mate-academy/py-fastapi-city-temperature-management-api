from fastapi import FastAPI

from database import Base, engine
from routers import cities, temperatures


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature API",
    description=(
        "CRUD-API"
    ),
    version="1.0.0",
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "docs": "/docs"}
