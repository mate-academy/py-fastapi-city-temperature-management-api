import logging

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.routers import cities, temperatures
from app.database import engine, Base
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.services.weather_service import close_http_client

logger = logging.getLogger(__name__)

app = FastAPI(
    title="City Temperature Management API",
    description="API for managing city data and their temperatures",
    version="1.0.0"
)

# Register routers
app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])


@app.get("/")
async def root():
    """
    Root endpoint for API health check.
    """
    return {
        "message": "City Temperature Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "cities": "/cities",
            "temperatures": "/temperatures"
        }
    }


@app.on_event("startup")
async def startup():
    """
    Creates database tables on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    """
    Closes database connections and HTTP client on application shutdown.
    
    Errors during shutdown are logged but don't crash the application
    to ensure a clean shutdown process.
    
    Note: In SQLAlchemy 2.0+, AsyncEngine.dispose() is awaitable.
    For older versions, use engine.sync_engine.dispose() instead.
    """
    # Close database connections
    try:
        await engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}", exc_info=True)
    
    # Close HTTP client
    try:
        await close_http_client()
        logger.info("HTTP client closed successfully")
    except Exception as e:
        logger.error(f"Error closing HTTP client: {e}", exc_info=True)


# Register error handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)  

