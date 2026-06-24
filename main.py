import uvicorn
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import cities, temperatures

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature Management API",
    description=(
        "A system for managing cities and synchronizing their "
        "current temperature through third-party services."
    ),
    version="1.0.0"
)

app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Weather API! Go to /docs to work with Swagger UI."
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
