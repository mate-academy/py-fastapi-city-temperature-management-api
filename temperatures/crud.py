from dependencies import SessionDep
from temperatures.models import Temperature


async def create_all_cities_temperature(
    db: SessionDep, temperatures: list[Temperature]
) -> list[Temperature]:
    db.add_all(temperatures)

    await db.commit()

    for temperature in temperatures:
        await db.refresh(temperature)

    return temperatures
