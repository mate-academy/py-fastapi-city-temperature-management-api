from fastapi import FastAPI
import logging

from city import router as city_router
from database import engine, Base
from temperature import router as temperature_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully")
except Exception as e:
    logger.error(f"Error creating tables: {e}")


app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)
