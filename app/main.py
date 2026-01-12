from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .api import cities, temperatures

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Temperature API",
    description="API for managing cities and their temperature data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cities.router, prefix="/api/v1", tags=["cities"])
app.include_router(temperatures.router, prefix="/api/v1", tags=["temperatures"])

@app.get("/")
async def root():
    return {
        "message": "City Temperature Management System",
        "docs": "/docs",
        "redoc": "/redoc"
    }
