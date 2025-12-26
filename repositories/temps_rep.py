from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import CityModel, Temperature
from database.sqlite import get_session, get_context
from meteo.open_meteo import get_temperature
from schemas.temps_schema import TempSchema, TempListSchema


async def get_rep():
    async with get_context() as session:
        yield TempRepository(session)


class TempRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_temps_by_city(self, city_id):
        smtp = select(Temperature)
        if city_id:
            smtp = smtp.where(Temperature.city_id == city_id)

        result = await self.session.execute(smtp)
        temps = result.scalars().all()
        temps = [TempSchema.model_validate(model) for model in temps]
        return TempListSchema(temps=temps)


    async def update_temps_for_all_cities(self):
        result = await self.session.execute(select(CityModel))
        cities = result.scalars().all()

        new_temps = []

        for city in cities:
            temp = await get_temperature(city.name)
            new_temps.append(Temperature(
                city_id=city.id,
                temperature=temp
            ))

        self.session.add_all(new_temps)
        await self.session.commit()
