from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import cities, temperatures

app = FastAPI(
    title="City & Temperature API",
    description=(
        "CRUD for cities and temperature history.\n\n"
        "Use POST /temperatures/update to fetch "
        "current temps for all cities via Open-Meteo."
    ),
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    # Create tables on application startup
    # to avoid side effects during imports/tests
    Base.metadata.create_all(bind=engine)


# CORS (optional, permissive for demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(cities.router)
app.include_router(temperatures.router)


@app.get("/healthz")  # tiny health check
def health():
    return {"status": "ok"}
