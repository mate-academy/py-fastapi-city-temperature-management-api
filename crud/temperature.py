from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.entities import Temperature, City
from schemas.temperature import TemperatureResponse
from datetime import datetime
import httpx


async def get_temperatures(db: AsyncSession, city_id: int = None) -> list[Temperature]:
    """Get all temperatures or filter by city_id"""
    query = select(Temperature)

    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()


async def fetch_temperature_for_city(city_name: str) -> float | None:
    """
    Fetch current temperature for a city using OpenWeatherMap API
    You can also use wttr.in as a free alternative
    """
    try:
        # Using wttr.in - free, no API key needed
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://wttr.in/{city_name}?format=j1", timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                temp_c = float(data["current_condition"][0]["temp_C"])
                return temp_c
            return None
    except Exception as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None


async def update_temperatures_for_all_cities(db: AsyncSession) -> dict:
    """Fetch and store temperatures for all cities in database"""
    # Get all cities
    result = await db.execute(select(City))
    cities = result.scalars().all()

    if not cities:
        return {
            "message": "No cities found in database",
            "updated_cities": 0,
            "temperatures_added": 0,
        }

    updated_count = 0
    temperatures_added = 0
    current_datetime = datetime.now().isoformat()

    # Fetch temperature for each city
    for city in cities:
        temperature = await fetch_temperature_for_city(city.name)

        if temperature is not None:
            # Create new temperature record
            new_temp = Temperature(
                city_id=city.id, date_time=current_datetime, temperature=temperature
            )
            db.add(new_temp)
            updated_count += 1
            temperatures_added += 1

    # Commit all changes
    await db.commit()

    return {
        "message": f"Successfully updated temperatures for {updated_count} cities",
        "updated_cities": updated_count,
        "temperatures_added": temperatures_added,
    }


async def create_temperature(
    db: AsyncSession, city_id: int, temperature: float
) -> Temperature:
    """Create a single temperature record"""
    current_datetime = datetime.now().isoformat()

    new_temp = Temperature(
        city_id=city_id, date_time=current_datetime, temperature=temperature
    )

    db.add(new_temp)
    await db.commit()
    await db.refresh(new_temp)

    return new_temp
