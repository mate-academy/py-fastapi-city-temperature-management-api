from sqlalchemy import text
from src.db.database import AsyncSessionLocal
from src.city.models import City


async def seed_data():
    async with AsyncSessionLocal() as session:
        existing_data = await session.execute(
            text("SELECT COUNT(*) FROM cities")
        )
        count = existing_data.scalar_one_or_none()
        if count and count > 8:
            print("Database already seeded.")
            return

        new_cities = [
            City(name="Los Angeles", additional_info="USA"),
            City(name="Chicago", additional_info="USA"),
            City(name="Houston", additional_info="USA"),
            City(name="Phoenix", additional_info="USA"),
            City(name="Philadelphia", additional_info="USA"),
            City(name="San Antonio", additional_info="USA"),
            City(name="San Diego", additional_info="USA"),
            City(name="Dallas", additional_info="USA"),
            City(name="San Jose", additional_info="USA"),
        ]
        session.add_all(new_cities)
        await session.commit()
        print(f"Inserted {len(new_cities)} new cities.")
