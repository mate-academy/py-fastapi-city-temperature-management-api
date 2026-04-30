import asyncio
from contextlib import asynccontextmanager
from alembic.config import Config
from alembic import command

from fastapi import FastAPI

from config import settings
from city.router import router as city_router
from temperature.router import router as temperature_router


@asynccontextmanager
async def initialize_db(app: FastAPI):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
    yield


app = FastAPI(lifespan=initialize_db)

app.include_router(city_router)
app.include_router(temperature_router)
