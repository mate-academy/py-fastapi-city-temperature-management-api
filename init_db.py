import asyncio
from database import AsyncSessionLocal, engine
import models
from sqlalchemy import text


async def init_db():
    async with engine.begin() as conn:
        # Drop all tables (careful!)
        await conn.run_sync(models.Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(models.Base.metadata.create_all)

    print("Database initialized!")


async def add_sample_cities():
    async with AsyncSessionLocal() as db:
        from crud import create_city
        from schemas import CityCreate

        sample_cities = [
            CityCreate(name="Moscow", additional_info="Capital of Russia"),
            CityCreate(name="London", additional_info="Capital of UK"),
            CityCreate(name="New York", additional_info="USA"),
            CityCreate(name="Tokyo", additional_info="Capital of Japan"),
            CityCreate(name="Paris", additional_info="Capital of France"),
        ]

        for city in sample_cities:
            existing = await db.execute(
                text("SELECT * FROM cities WHERE name = :name"),
                {"name": city.name}
            )
            if not existing.fetchone():
                await create_city(db, city)

        await db.commit()
        print("Sample cities added!")


if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(add_sample_cities())
