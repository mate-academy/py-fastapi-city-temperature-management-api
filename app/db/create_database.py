from db.database import Base, AsyncSessionGenerator, async_engine
from db.models import CityORM


async def create_tables():
    async with async_engine.begin() as db:
        await db.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with async_engine.begin() as db:
        await db.run_sync(Base.metadata.drop_all)


async def insert_data():
    cities = [
        CityORM(
            name="London",
            additional_info="The city is blanketed in a light mist with persistent drizzle and cool, damp air throughout the day."
        ),
        CityORM(
            name="Paris",
            additional_info="Expect clear blue skies and mild sunshine with a gentle breeze blowing across the Seine."
        ),
        CityORM(
            name="New York",
            additional_info="Bright but chilly conditions prevail with high winds whistling between the skyscrapers."
        ),
        CityORM(
            name="Tokyo",
            additional_info="Humid and warm weather with occasional light showers and a heavily overcast sky."
        ),
        CityORM(
            name="Rome",
            additional_info="Golden sunlight bathes the city with warm temperatures and perfectly still, dry air."
        )
    ]
    async with AsyncSessionGenerator() as db:
        db.add_all(cities)
        await db.commit()