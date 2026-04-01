from asyncio import run
from db.create_database import create_tables, drop_tables
from db.database import async_engine


async def initialize_db():
    await drop_tables()
    await create_tables()
    await async_engine.dispose()

run(initialize_db())