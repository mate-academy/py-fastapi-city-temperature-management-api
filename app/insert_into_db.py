from asyncio import run
from db.create_database import insert_data
from db.database import async_engine

async def insert():
    await insert_data()
    await async_engine.dispose()

run(insert())